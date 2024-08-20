generate:
  ../flatbuffers/build/flatc --cpp --python --python-gen-numpy --python-typing --rust --gen-all CityBufFeature.fbs

test:
  python cjseq2cb.py data/one_feature.city.jsonl data/one_feature.cb
  python load_citybuf.py data/one_feature.cb

cb2j:
  python cb2cjseq.py data/one_feature.cb data/one_feature_out.city.jsonl