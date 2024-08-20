generate:
  ../flatbuffers/build/flatc --cpp --python --python-gen-numpy --python-typing --rust --gen-all CityBufFeature.fbs

test_roundtrip:
  python cjseq2cb.py data/one_feature.city.jsonl data/one_feature.cb
  python cb2cjseq.py data/one_feature.cb data/one_feature_out.city.jsonl

test_equalise:
  jq -S . data/one_feature.city.jsonl > data/one_feature_sort.city.jsonl
  jq -S . data/one_feature_out.city.jsonl > data/one_feature_out_sort.city.jsonl

test_diff:
  diff data/one_feature_sort.city.jsonl data/one_feature_out_sort.city.jsonl || true

test: test_roundtrip test_equalise test_diff