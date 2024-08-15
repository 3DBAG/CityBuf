# CityBuf Introduction
Binary format to efficiently store [CityJSONSequences](https://www.cityjson.org/cityjsonseq/). Inspired by the [FlatGeobuf](https://github.com/flatgeobuf/flatgeobuf) standard (which in turn uses [flatbuffers](https://github.com/google/flatbuffers)).

## Goals
The primary goals of CityBuf:
1. be very fast to write/read
2. have a very low memory footprint wile reading large files
3. Lossless conversion to/from CityJSONSequence files (.city.jsonl)
4. use strongly typed attributes. This prevents type ambiguity as can happen with cityjson (eg 3DBV dataset has several issues, eg. inconsistent objectid (both string and int is used), or all values of an attribute are `null` (so not possible to deduce type)). This is important for lossles conversion to GIS formats (eg `gpkg`), and other reading application where strong types are relevant.

Secondary goals:
1. small file size (but, without compromising reading speed, so no compression etc)

Don't really care:
1. Efficient in-place modifications of existing files
2. Quick and DB like attribute access. Ie. this is not a column based format, focus is on feature-by-feature access in a streaming fashion, same as CityJSONSequences.

## references
- CityJSON
  - https://www.cityjson.org/specs/2.0.1/
  - https://www.cityjson.org/cityjsonseq/
  - https://www.cityjson.org/dev/geom-arrays/
- FlatGeobuf
  - https://github.com/flatgeobuf/flatgeobuf
  - https://worace.works/2022/02/23/kicking-the-tires-flatgeobuf/ (recommended reading about the cool features of flatbuffers/FlatGeoBuf)
  - https://worace.works/2022/03/12/flatgeobuf-implementers-guide/
  - reference implementations attribute buffers:
    - https://github.com/gogama/flatgeobuf/blob/main/flatgeobuf/prop_reader.go
    - https://github.com/OSGeo/gdal/blob/master/ogr/ogrsf_frmts/flatgeobuf/ogrflatgeobuflayer.cpp#L2058
- flatbuffers
  - https://github.com/google/flatbuffers
  - https://flatbuffers.dev/flatbuffers_guide_writing_schema.html
  - https://flatbuffers.dev/flatbuffers_internals.html

# CityBuf file layout
A CityBuf (`.cb`) file is binary encoded and consists of the following parts (very similar to flatgeobuf):

1. Magic bytes. The first 8 bytes of a CityBuf file are a signature, containing: ASCII `FCB`, followed by the spec major version (currently 00), then `FCB` again, then the spec patch version (currently 02).
2. Header. A length-prefixed flatbuffer Header record (see `CityBufHeader.fbs`)
3. Data. A concatenation of length-prefixed flabuffer records (see `CityBufFeature.fbs`).

The length prefixes are `Uint32`.

Any 64-bit flatbuffer value contained anywhere in the file (for example coordinates) is aligned to 8 bytes to from the start of the file or feature to allow for direct memory access.

Encoding of any string value is assumed to be UTF-8.

## CityBufFeatures
The features in the Data portion of an CityBuf file are modelled after [CityJSONFeatures](https://www.cityjson.org/specs/2.0.1/#text-sequences-and-streaming-with-cityjsonfeature). There is support for all the CityJSON geometry types and Semantic surfaces. Not supported are Geometry templates, Appearance and Extensions. One should be able to do a lossless conversion to/from CityJSON features (excluding the unsupported features for now).

## Attributes
To store attribute values we adopt [the approach from flatgeobuf](https://worace.works/2022/03/12/flatgeobuf-implementers-guide/#properties-schema-representation-columns-and-columntypes): a column schema that is stored in the columns vector field in the header (or optionally inside the features, in case  attributes are different for each feature) and a custom binary `attributes` buffer that contains the attribute values and references the column schema, ie each value is encoded as:

- u16 (2 bytes) column index — this indicates the “key”, by way of pointing to the index of the appropriate column in the Columns vector
- Appropriate per-type binary representation. Depending on the ColumnType, sometimes these are statically sized and sometimes they include a length prefix. So for a Bool column it will always be 3 bytes — 2 for the index and 1 for the bool itself (u8, little-endian). For a String, it’s variable, with 2 bytes for the column index, then a 4-byte unsigned length, then a UTF-8 encoding of the String.

# Implementation status
Currently the whole CityBuf specification has been implemented in python. This includes
  - `cjseq2citybuf.py`: a script to convert `.city.jsonl` to a `.cb` file.
  - `attributes.py`: python code to encode and decode the custom attribute buffers
  - a simple `CityBufReader` class that allows for convenient access of the flatbuffer records
  - a `load_citybuf.py` for the Benchmark (see below). This is also an example for how to use the `CityBufReader` class.

What is missing:
 - script to convert from `.cb` to `.city.jsonl`
 - other languages than python, eg. C++. Notice that this repository does include automatically generated flatbuffer accessor/build functions for python, c++ and rust. But to make it convenient to build and read CityBuf files, some convenient wrappers are needed.

 Other TODO:
 - review header metadata specification, make sure this is fully compatible with CityJSON

# Benchmark
This Benchmark compares CityBuf to CityJSON and CityJSONSequence. It compares the file size of the three formats for a variety of datasets, and a read test is performed, which gives us an idea of read speed and memory consumption during reading.

Summary of main findings:
- CityBuf is always the fastest in the read test. Overall nearly 80% faster than CityJSON and 59% faster than CityJSONSeq.
- In case of large features (3DBV dataset) the memory consumption of CityBuf is significantly lower.
- CityBuf always gives the smallest file size. Overall 34% smaller than CityJSON and 18% smaller than CityJSONSeq.

Table below gives the full results.

This is an extension of the benchmark given in https://github.com/cityjson/paper_cjseq. Some dataset were excluded:
- Railway is not included because it uses geometry templates. 
- Helsinki_tex not included because it uses textures. 
Both features are currently not supported in CityBuf so not fair to include/compare.

All using a python implementation on MacOS. CPU: M1 Pro 12 Core.

**NB** the max RSS also includes program code, which in case of CityBuf is already 21MB (ie. this is the RSS just after the `import`s and before running the actual benchmark), therefore 21MB is the minimum RSS value in the table for CityBuf. The RSS values are therefore not representative of just the in-memory size of the loaded city objects, especially for the smaller datasets.

| Dataset     | Format        | Read test Max RSS (MB) | Read test runtime (s) | File Size (MB) |
|-------------|---------------|------------------------| ----------------------|----------------|
| **3DBAG**   | CityJSON      | `76.52`                | `0.14`                | `6.7`          |
|             | CityJSONSeq   | `16.50`                | `0.10`                | `5.9`          |
|             | CityBuf       | `21.52`                | `0.08`                | `4.5`          |
| **3DBV**    | CityJSON      | `3822.67`              | `7.57`                | `378`          |
|             | CityJSONSeq   | `137.27`               | `3.97`                | `317`          |
|             | CityBuf       | `38.94`                | `0.92`                | `285`          |
| **Helsinki**| CityJSON      | `3760.11`              | `7.48`                | `572`          |
|             | CityJSONSeq   | `16.03`                | `3.37`                | `412`          |
|             | CityBuf       | `22.30`                | `1.22`                | `316`          |
| **Ingolstadt**| CityJSON    | `65.94`                | `0.09`                | `4.8`          |
|             | CityJSONSeq   | `21.73`                | `0.08`                | `3.8`          |
|             | CityBuf       | `22.53`                | `0.06`                | `3.3`          |
| **Montréal**| CityJSON      | `79.11`                | `0.12`                | `5.4`          |
|             | CityJSONSeq   | `20.48`                | `0.10`                | `4.6`          |
|             | CityBuf       | `21.41`                | `0.05`                | `2.1`          |
| **NYC**     | CityJSON      | `937.70`               | `1.46`                | `105`          |
|             | CityJSONSeq   | `17.47`                | `0.83`                | `95 `          |
|             | CityBuf       | `21.77`                | `0.35`                | `78 `          |
| **Rotterdam**| CityJSON     | `42.56`                | `0.06`                | `2.6`          |
|             | CityJSONSeq   | `14.48`                | `0.06`                | `2.7`          |
|             | CityBuf       | `22.27`                | `0.06`                | `1.2`          |
| **Vienna**  | CityJSON      | `59.39`                | `0.09`                | `5.4`          |
|             | CityJSONSeq   | `16.59`                | `0.08`                | `4.8`          |
|             | CityBuf       | `21.59`                | `0.07`                | `4.2`          |
| **Zurich**  | CityJSON      | `2814.70`              | `5.30`                | `279`          |
|             | CityJSONSeq   | `18.34`                | `2.45`                | `247`          |
|             | CityBuf       | `22.33`                | `1.73`                | `197`          |

The sum of the file sizes grouped by format is:
- **CityJSON**: 1358.9 MB
- **CityJSONSeq**: 1092.8 MB
- **CityBuf**: 891.3 MB

The sum of the runtimes grouped by format is:
- **CityJSON**: 22.31 seconds
- **CityJSONSeq**: 11.04 seconds
- **CityBuf**: 4.54 seconds

# Ideas for future work
- Implement a spatial index, could be the same as FlatGeofbuf
- Implement an Feature ID index
- See if we can effciently access large CityBuf files over the web using HTTP range requests (same as FlatGeoBuf), probably need to implement spatial index first.
- Investigate/Add support for CityJSON geometry templates, textures and extensions
- Could try to reuse the same strings within a feature, instead of always creating a new string even if the same string occurs many times.
- Look at support for enum attributes