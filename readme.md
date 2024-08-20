# CityBuf Introduction
Binary variant of [CityJSONSeq](https://www.cityjson.org/cityjsonseq/). Inspired by the [FlatGeobuf](https://github.com/flatgeobuf/flatgeobuf) standard (which in turn uses [flatbuffers](https://github.com/google/flatbuffers)).

- overall ~5x faster than CityJSON and ~2x faster than CityJSONSeq in a simple read test,
- significantly lower memory usage than CityJSON and CityJSONSeq in simple read test (especially for large features),
- overall 34% smaller files than CityJSON and 18% smaller than CityJSONSeq.

These number are based on the benchmark that is given in more detail below.

__WORK IN PROGRESS!!__: this spec is not finalised yet

## Goals
The primary goals of CityBuf are
1. be very fast to write/read features in a streaming fashion,
2. have a very low memory footprint wile reading large files,
3. lossless conversion to/from CityJSONSeq files (.city.jsonl),
4. use strongly typed attributes. This prevents type ambiguity as can happen with cityjson (eg 3DBV dataset has several issues, eg. inconsistent objectid (both string and int is used), or all values of an attribute are `null` (so not possible to deduce type)). This is important for lossles conversion to GIS formats (eg `gpkg`), and other reading applications where strong types are relevant.

Don't really care:
1. efficient in-place modifications of existing files
2. quick and DB like attribute access. Ie. this is not a column based format, focus is on feature-by-feature access in a streaming fashion, same as CityJSONSeq.

# CityBuf file layout
A CityBuf (`.cb`) file is binary encoded and consists of the following parts (very similar to flatgeobuf):

1. Magic bytes. The first 8 bytes of a CityBuf file are a signature, containing: ASCII `FCB`, followed by the spec major version (currently 00), then `FCB` again, then the spec patch version (currently 02).
2. Header. A length-prefixed flatbuffer Header record (see `CityBufHeader.fbs`)
3. Data. A concatenation of length-prefixed flatbuffer CityFeature records (see `CityBufFeature.fbs`).

The length prefixes are `Uint32`.

Any 64-bit flatbuffer value contained anywhere in the file (for example coordinates) is aligned to 8 bytes from the start of the file or feature to allow for direct memory access.

Encoding of any string value is assumed to be UTF-8.

## CityFeatures
The features in the Data portion of an CityBuf file are modelled after [CityJSONFeatures](https://www.cityjson.org/specs/2.0.1/#text-sequences-and-streaming-with-cityjsonfeature). There is support for all the CityJSON geometry types and Semantic surfaces. One should be able to do a lossless conversion to/from CityJSON features (excluding the unsupported features).

 Currently not supported are CityJSON's geometry templates, appearance and extensions. However, these features will be added in the future.

## Geometry
Given this `Solid` with 2 shells in the CityJSON encoding:
```
boundaries: [
  [ [[0, 3, 2, 1, 22], [1, 2, 3, 4]], [[4, 5, 6, 7]], [[0, 1, 5, 4]], [[1, 2, 6, 5]] ], 
  [ [[240, 243, 124]], [[244, 246, 724]], [[34, 414, 45]], [[111, 246, 5]] ]
]
```

CityBuf will encode this Solid using a number of flat arrays:
```
indices:  [0, 3, 2, 1, 22, 1, 2, 3, 4, 4, 5, 6, 7, 0, 1, 5, 4, 1, 2, 6, 5, 240, 243, 124, 244, 246, 724, 34, 414, 45, 111, 246, 5] # flat list of indices
strings:  [5, 4, 4, 4, 4, 3, 3, 3, 3] # number of indices per ring, sum should equal length of indices array
surfaces: [2, 1, 1, 1, 1, 1, 1, 1] # 8 surfaces, 1st has 2 rings, the rest all have 1 ring
shells:   [4, 4] # 2 shells that each consist of 4 surfaces
solids:   [2] # one solid that consists of two shells
```

Which of these arrays have values, will depend on the geometry type. Notice that the `strings` array is used both for the Rings of a Surface, and the LineStrings of a MultiLineString.

Semantic values are also encoded using a flat array, similar to the `indices`.

`geometry.py` gives an implementation of how to go back and forth between these 2 representations.

Specificalities:
- `null` values in the geometry semantic values list are encoded as the maximum value of a `Uint32`.

## Attributes
To store attribute values we adopt [the approach from flatgeobuf](https://worace.works/2022/03/12/flatgeobuf-implementers-guide/#properties-schema-representation-columns-and-columntypes): a column schema that is stored in the columns vector field in the header (or optionally inside the features, in case  attributes are different for each feature) and a custom binary `attributes` buffer that contains the attribute values and references the column schema, ie each value is encoded as:

- u16 (2 bytes) column index — this indicates the “key”, by way of pointing to the index of the appropriate column in the Columns vector
- Appropriate per-type binary representation. Depending on the ColumnType, sometimes these are statically sized and sometimes they include a length prefix. So for a Bool column it will always be 3 bytes — 2 for the index and 1 for the bool itself (u8, little-endian). For a String, it’s variable, with 2 bytes for the column index, then a 4-byte unsigned length, then a UTF-8 encoding of the String.

Attributes that have a `null` value can be explitly encoded using 4 bytes:
- u16 (2 bytes) max value of a uint16
- u16 (2 bytes) column index

# Benchmark
This Benchmark compares CityBuf to CityJSON and CityJSONSeq. It compares the file size of the three formats for a variety of datasets, and a read test is performed, which gives us an idea of read speed and memory consumption during reading.

This is an extension of the benchmark given in https://github.com/cityjson/paper_cjseq. Some dataset were excluded:
- Railway is not included because it uses geometry templates. 
- Helsinki_tex included because it uses textures. (TODO: remove Rotterdam/Montréal they also have textures)

Both features are currently not supported in CityBuf so not fair to include/compare. 

All using a python implementation on MacOS. CPU: M1 Pro 12 Core.

**NB** the max RSS also includes program code, which in case of CityBuf is already 21MB (ie. this is the RSS just after the `import`s and before running the actual benchmark), therefore 21MB is the minimum RSS value in the table for CityBuf. The RSS values are therefore not representative of just the in-memory size of the loaded city objects, especially for the datasets with small features.

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

# Implementation status
There are the following Python scripts:
- `cb2cjseq.py`: a script to convert `.cb` to a `.city.jsonl` file
- `cjseq2cb.py`: a script to convert `.city.jsonl` to a `.cb` file.
- `attributes.py`: python code to encode and decode the custom attribute buffers. Atm only the most common attribute types are implemented (bool, int, float, string, json).
- `geometry.py`: python code to convert between CityJSON and CityBuf geometry representation
- a simple `CityBufReader` class that allows for convenient access of the flatbuffer records
- a `load_citybuf.py` the read test for the benchmark. This is also an example for how to use the `CityBufReader` class.

Other languages than Python, eg. C++, have so far received no attention. Notice that this repository does include automatically generated flatbuffer accessor/build functions for python, C++ and Rust. But to make it convenient to build and read CityBuf files, some convenient wrappers are needed.

TODO:
 - implement encoding/decoding of remaining attribute types
 - review header metadata specification, make sure this is fully compatible with CityJSONSeq

## Usage of conversion scripts
To convert from `.city.jsonl` to `.cb`:
```sh
python cjseq2cb.py data/one_feature.city.jsonl data/one_feature.cb
```
See `python cjseq2cb.py --help` for more options.

To convert from `.cb` to `.city.jsonl`:
```sh
python cb2cjseq.py data/one_feature.cb data/one_feature_out.city.jsonl
```

# Ideas for future work
- Implement a spatial index, could be the same as FlatGeoBuf
- Implement an Feature ID index
- See if we can effciently access large CityBuf files over the web using HTTP range requests (same as FlatGeoBuf), probably need to implement spatial index first.
- Do more extensive benchamrking
- Investigate and implement support for CityJSON extensions
- Add support for geometry templates
- Add support for textures
- Could try to reuse the same attribute value strings within a feature, instead of always creating a new string even if the same string occurs many times.
- Look at support for enum attributes


## References
- CityJSON(Sequences)
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