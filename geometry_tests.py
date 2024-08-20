from geometry import GeometryEncoder, GeometryDecoder, GeometryType

compositesolid_testcase = GeometryType.CompositeSolid, [
  [ 
    [ [[0, 3, 2, 1, 22]], [[4, 5, 6, 7]], [[0, 1, 5, 4]], [[1, 2, 6, 5]] ],
    [ [[240, 243, 124]], [[244, 246, 724]], [[34, 414, 45]], [[111, 246, 5]] ]
  ],
  [ 
    [ [[666, 667, 668]], [[74, 75, 76]], [[880, 881, 885]], [[111, 122, 226]] ] 
  ]    
]
multisolid_testcase = GeometryType.MultiSolid, [
  [ 
    [ [[0, 3, 2, 1, 22]], [[4, 5, 6, 7]], [[0, 1, 5, 4]], [[1, 2, 6, 5]] ],
    [ [[240, 243, 124]], [[244, 246, 724]], [[34, 414, 45]], [[111, 246, 5]] ]
  ],
  [ 
    [ [[666, 667, 668]], [[74, 75, 76]], [[880, 881, 885]], [[111, 122, 226]] ] 
  ]    
]
solid_testcase = GeometryType.Solid, [
  [ [[0, 3, 2, 1, 22], [1,2,3,4]], [[4, 5, 6, 7]], [[0, 1, 5, 4]], [[1, 2, 6, 5]] ], 
  [ [[240, 243, 124]], [[244, 246, 724]], [[34, 414, 45]], [[111, 246, 5]] ]
]
multisurface_testcase = GeometryType.MultiSurface, [
  [ [1, 2, 3, 4, 5], [6, 8, 7], [9, 12, 11, 10] ], [[14, 15, 16]]
]
compositesurface_testcase = GeometryType.CompositeSurface, [
  [[0, 3, 2, 1]], [[4, 5, 6, 7]], [[0, 1, 5, 4]]
]
multipoint_testcase = GeometryType.MultiPoint, [2, 44, 0, 7]
multilinestring_testcase = GeometryType.MultiLineString, [
  [2, 3, 5], [77, 55, 212]
]

def test_all():
  test(compositesolid_testcase)
  test(multisolid_testcase)
  test(solid_testcase)
  test(multisurface_testcase)
  test(compositesurface_testcase)
  test(multipoint_testcase)
  test(multilinestring_testcase)

def test(testcase):
  t, bnds = testcase
  encoder = GeometryEncoder()
  encoder.encode(bnds)
  print("indices: ", encoder.indices)
  print("strings: ", encoder.strings)
  print("surfaces: ", encoder.surfaces)
  print("shells: ", encoder.shells)
  print("solids: ", encoder.solids)
  print("ibounds", bnds)
  decoder = GeometryDecoder(encoder.indices, encoder.strings, encoder.surfaces, encoder.shells, encoder.solids)
  obnds = decoder.decode(t)
  print("obounds", obnds)
  assert obnds == bnds

test_all()