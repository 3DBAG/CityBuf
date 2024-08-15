# FlatCityBuf

Binary format to efficiently store city objects inspired by CityJSON and FlatGeobuf (which in turn uses flatbuffers).

## references

- https://github.com/flatgeobuf/flatgeobuf
- https://worace.works/2022/02/23/kicking-the-tires-flatgeobuf/
- https://worace.works/2022/03/12/flatgeobuf-implementers-guide/

- https://www.cityjson.org/specs/2.0.1/

- https://github.com/google/flatbuffers

## Design
A FlatCityBuf (fcb) file is binary encoded and has the following parts (very similar to flatgeobuf):

1. Magic byte CB. The first 6 bytes of a cb file are a signature, containing: ASCII C, B, followed by the spec major version (currently 01), then C,B again, then the spec patch version (currently 00).
2. Header, see `FCBHeader.fbs`, a length-prefixed flatbuffer record
3. Data, see `FCBFeature.fbs`. a concatenation of length-prefixed flabuffer records.

length prefixes are Uint32.

Any 64-bit flatbuffer value contained anywhere in the file (for example coordinates) is aligned to 8 bytes to from the start of the file or feature to allow for direct memory access.

Encoding of any string value is assumed to be UTF-8.

### CityJSONFeatures
The features in the Data portion of an fcb file are modelled after CityJSONFeatures. There is support for all the CityJSON geometry types and Semantic surfaces. Not supported are Geometry templates, Appearance and Extensions. One goal is to be able to do a lossless conversion to/from CityJSON features (excl appearance and extensions for now).

### Attributes
To store attribute values we adopt the approach from flatgeobuf: an column schema that is stored in the columns vector field in the header (or locally inside the features, eg if  attributes are different for each feature) and a custom binary `attributes` buffer that contains the attribute values and references the column schema, ie each value is encoded as:
```
- u16 (2 bytes) column index — this indicates the “key”, by way of pointing to the index of the appropriate column in the Columns vector
- Appropriate per-type binary representation. Depending on the ColumnType, sometimes these are statically sized and sometimes they include a length prefix. So for a Bool column it will always be 3 bytes — 2 for the index and 1 for the bool itself (u8, little-endian). For a String, it’s variable, with 2 bytes for the column index, then a 4-byte unsigned length, then a UTF-8 encoding of the String.
```

## vs cityjson
- use enums for types insteads of repeating same string many times
- binary
- type is always known, no ambiguity as with cityjson (eg 3DBV has inconsistent objectid either string or int)

## further optimisation
use smallest possible number type for indices?

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