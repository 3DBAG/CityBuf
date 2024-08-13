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

1. Magic byte FCB. The first 8 bytes of a fcb file are a signature, containing: ASCII F , C, B, followed by the spec major version (currently 01), then F,C,B again, then the spec patch version (currently 00).
2. Header, see `FCBHeader.fbs`, a length-prefixed flatbuffer record
3. Data, see `FCBFeature.fbs`. a concatenation of length-prefixed flabuffer records.

length prefixes are Uint32.

Any 64-bit flatbuffer value contained anywhere in the file (for example coordinates) is aligned to 8 bytes to from the start of the file or feature to allow for direct memory access.

Encoding of any string value is assumed to be UTF-8.

### CityJSONFeatures
The features in the Data portion of an fcb file are modelled after CityJSONFeatures. There is support for all the CityJSON geometry types and Semantic surfaces. Not supported are Appearance and Extensions. One goal is to be able to do a lossless conversion to/from CityJSON features (excl appearance and extensions for now).

### Attributes
To store attribute values we adopt the approach from flatgeobuf: an column schema that is stored in the columns vector field in the header (or locally inside the features, eg if  attributes are different for each feature) and a custom binary `attributes` buffer that contains the attribute values and references the column schema, ie each value is encoded as:
```
- u16 (2 bytes) column index — this indicates the “key”, by way of pointing to the index of the appropriate column in the Columns vector
- Appropriate per-type binary representation. Depending on the ColumnType, sometimes these are statically sized and sometimes they include a length prefix. So for a Bool column it will always be 3 bytes — 2 for the index and 1 for the bool itself (u8, little-endian). For a String, it’s variable, with 2 bytes for the column index, then a 4-byte unsigned length, then a UTF-8 encoding of the String.
```

## vs cityjson
- use enums for types insteads of repeating same string many times
- binary
- type is always known, no ambiguity as with cityjson

## further optimisation
use smallest possible number type for indices?