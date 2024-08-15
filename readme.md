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
To store attribute values we adopt [the approach from flatgeobuf](https://worace.works/2022/03/12/flatgeobuf-implementers-guide/#properties-schema-representation-columns-and-columntypes): an column schema that is stored in the columns vector field in the header (or optionally inside the features, in case  attributes are different for each feature) and a custom binary `attributes` buffer that contains the attribute values and references the column schema, ie each value is encoded as:
```
- u16 (2 bytes) column index — this indicates the “key”, by way of pointing to the index of the appropriate column in the Columns vector
- Appropriate per-type binary representation. Depending on the ColumnType, sometimes these are statically sized and sometimes they include a length prefix. So for a Bool column it will always be 3 bytes — 2 for the index and 1 for the bool itself (u8, little-endian). For a String, it’s variable, with 2 bytes for the column index, then a 4-byte unsigned length, then a UTF-8 encoding of the String.
```
Compared to CityJSON this reduces the required storage size and reading speed especially in case we have many feature with the same set of attributes (no need to repeat/read the same attribute names many times).

# Implementation status
Currently the whole CityBuf standard has been implemented in python. This includes
  - `cjseq2citybuf.py`: a script to convert `.city.jsonl` to a `.cb` file.
  - `attributes.py`: python code to encode and decode the custom attribute buffers
  - a simple `CityBufReader` class that allows for convenient access of the flatbuffer records
  - a `load_citybuf.py` for the Benchmark (see below). This is also an example for how to use the `CityBufReader` class.

What is missing:
 - script to convert from `.cb` to `.city.jsonl`
 - other languages than python, eg. C++. Notice that this repository does include automatically generated flatbuffer accessor/build functions for python, c++ and rust. But to make it convenient to build and read CityBuf files, some convenient wrappers are needed. In 

 Other TODO:
 - review header metadata specification, make sure this is fully compatible with CityJSON

# Benchmark
Based on https://github.com/cityjson/paper_cjseq.

- Railway is not included because it uses geometry templates. 
- Helsinki_tex not included because it uses textures. 

Both features are currently not supported in CityBuf so not fair to include/compare.

## RSS memory usage and time
- NB: In python importing flatbuffers module increases rss already with ~10MB. Together with other imported modules this means the RSS starts at around 21MB before reading any CityBuf data.

Below the results (max RSS and runtime) for each dataset are given in the following order:
1. CityJSON
1. CityJSONSequence
1. CityBuf

All using a python implementation

```
==3DBAG
76.515625
        0.14 real         0.12 user         0.01 sys
16.5
        0.10 real         0.08 user         0.00 sys
21.515625
        0.08 real         0.07 user         0.01 sys
==3DBV
3822.671875
        7.57 real         6.41 user         0.94 sys
137.265625
        3.97 real         3.82 user         0.13 sys
38.9375
        0.92 real         0.84 user         0.07 sys
==Helsinki
3760.109375
        7.48 real         7.00 user         0.35 sys
16.03125
        3.37 real         3.25 user         0.10 sys
22.3125
        1.22 real         1.12 user         0.09 sys
==Ingolstadt
65.9375
        0.09 real         0.08 user         0.00 sys
21.734375
        0.08 real         0.07 user         0.00 sys
22.53125
        0.06 real         0.04 user         0.00 sys
==Montréal
79.109375
        0.12 real         0.10 user         0.01 sys
20.484375
        0.10 real         0.08 user         0.00 sys
21.40625
        0.05 real         0.04 user         0.00 sys
==NYC
937.703125
        1.46 real         1.37 user         0.07 sys
17.46875
        0.83 real         0.79 user         0.03 sys
21.765625
        0.35 real         0.31 user         0.03 sys
==Rotterdam
42.5625
        0.06 real         0.05 user         0.00 sys
14.484375
        0.06 real         0.05 user         0.00 sys
22.265625
        0.06 real         0.05 user         0.00 sys
==Vienna
59.390625
        0.09 real         0.07 user         0.00 sys
16.59375
        0.08 real         0.07 user         0.00 sys
21.59375
        0.07 real         0.05 user         0.01 sys
==Zurich
2814.703125
        5.30 real         4.97 user         0.22 sys
18.34375
        2.45 real         2.35 user         0.07 sys
22.328125
        1.73 real         1.66 user         0.06 sys
```

## File sizes
```
4.5M 3DBAG.cb
6.7M 3DBAG.city.json
5.9M 3DBAG.city.jsonl
285M 3DBV.cb
378M 3DBV.city.json
317M 3DBV.city.jsonl
316M Helsinki.cb
572M Helsinki.city.json
412M Helsinki.city.jsonl
3.3M Ingolstadt.cb
4.8M Ingolstadt.city.json
3.8M Ingolstadt.city.jsonl
2.1M Montréal.cb
5.4M Montréal.city.json
4.6M Montréal.city.jsonl
 78M NYC.cb
105M NYC.json
 95M NYC.jsonl
1.2M Rotterdam.cb
2.6M Rotterdam.json
2.7M Rotterdam.jsonl
4.2M Vienna.cb
5.4M Vienna.city.json
4.8M Vienna.city.jsonl
197M Zurich.cb
279M Zurich.city.json
247M Zurich.city.jsonl
```

## Conclusion Benchmark
- CityBuf always gives (significantly) smaller file sizes
- CityBuf is faster to read/access
- In case of large features (3DBV dataset) the memory consumption of CityBuf is also significantly lower.

# Ideas for future work
- Implement a spatial index, could be the same as FlatGeofbuf
- Implement an Feature ID index
- See if we can effciently access large CityBuf files over the web using HTTP range requests (same as FlatGeoBuf), probably need to implement spatial index first.
- Could try to reuse the same strings within a feature, instead of always creating a new string even if the same string occurs many times.
- Look at support for enum attributes