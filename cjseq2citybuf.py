import json

from flatCitybuf import \
  Header, \
  CityFBFeature,  \
  CityObject,  \
  Crs,  \
  Geometry,  \
  Solid,  \
  Boundaries,  \
  Shell,  \
  Ring,  \
  Surface,  \
  MultiSurface,  \
  CompositeSurface,  \
  MultiSolid,  \
  CompositeSolid,  \
  MultiLineString, \
  LineString, \
  MultiPoint,  \
  Point,  \
  SemanticObject,  \
  Column,  \
  Vector
from flatCitybuf.SemanticSurfaceType import SemanticSurfaceType
from flatCitybuf.CityObjectType import CityObjectType
from flatCitybuf.Vertex import CreateVertex
from flatCitybuf.Transform import CreateTransform
from flatCitybuf.GeographicalExtent import CreateGeographicalExtent
import flatbuffers

import struct
import argparse, logging
import numpy as np

from attributes import AttributeSchemaEncoder, AttributeSchemaDecoder

def create_magic_bytes(major=0, minor=1):
  cb = "CB".encode('ascii')
  ma = major.to_bytes(1, byteorder='little')
  mi = minor.to_bytes(1, byteorder='little')

  # Convert ASCII string to bytes
  return cb + ma + cb + mi

def get_attribute_by_name(class_type, attribute_name):
    return getattr(class_type, attribute_name, None)

def create_point(builder, index, semantics_id=None):
  Point.Start(builder)
  Point.AddIndex(builder, index)
  if semantics_id:
    Point.AddSemanticObjectId(builder, semantics_id)
  return Point.End(builder)

def create_multipoint(builder, boundaries, semantics_values=None):
  f_points = []
  if semantics_values:
    for index, sem in zip(boundaries, semantics_values):
      f_points.append(create_point(builder, index, sem))
  else:
    for index in boundaries:
      f_points.append(create_point(builder, index))

  MultiPoint.StartPointsVector(builder, len(f_points))
  for point_offset in reversed(f_points):
    builder.PrependUOffsetTRelative(point_offset)
  f_points_offset = builder.EndVector()

  MultiPoint.Start(builder)
  MultiPoint.AddPoints(builder, f_points_offset)
  return MultiPoint.End(builder)

def create_linestring(builder, boundaries, semantics_id=None):
  LineString.StartIndicesVector(builder, len(boundaries))
  for index in reversed(boundaries):  # FlatBuffers requires reverse order when creating vectors
    builder.PrependUint32(index)
  f_indices_offset = builder.EndVector()

  LineString.Start(builder)
  LineString.AddIndices(builder, f_indices_offset)
  if semantics_id:
    LineString.AddSemanticObjectId(builder, semantics_id)
  return LineString.End(builder)

def create_multilinestring(builder, boundaries, semantics_values=None):
  f_linestrings = []
  if semantics_values:
    for linestring, sem in zip(boundaries, semantics_values):
      f_linestrings.append(create_linestring(builder, linestring, sem))
  else:
    for linestring in boundaries:
      f_linestrings.append(create_linestring(builder, linestring))
  
  MultiLineString.StartLineStringsVector(builder, len(f_linestrings))
  for linestring_offset in reversed(f_linestrings):
    builder.PrependUOffsetTRelative(linestring_offset)
  return builder.EndVector()

def create_ring(builder, boundaries):
  Ring.StartIndicesVector(builder, len(boundaries))
  for index in reversed(boundaries):  # FlatBuffers requires reverse order when creating vectors
    builder.PrependUint32(index)
  f_indices_offset = builder.EndVector()

  Ring.Start(builder)
  Ring.AddIndices(builder, f_indices_offset)
  return Ring.End(builder)

def create_surface(builder, boundaries, semantics_id=None):
  f_rings = []
  for ring in boundaries:
    f_rings.append(create_ring(builder, ring))
  
  Surface.StartRingsVector(builder, len(f_rings))
  for ring_offset in reversed(f_rings):
    builder.PrependUOffsetTRelative(ring_offset)
  f_rings_offset = builder.EndVector()

  Surface.Start(builder)
  Surface.AddRings(builder, f_rings_offset)
  if semantics_id:
    Surface.AddSemanticObjectId(builder, semantics_id)
  return Surface.End(builder)

def create_shell(builder, boundaries, semantics_values=None):
  f_surfaces = []
  if semantics_values:
    for surface, sem in zip(boundaries, semantics_values):
      f_surfaces.append(create_surface(builder, surface, sem))
  else:
    for surface in boundaries:
      f_surfaces.append(create_surface(builder, surface))
  
  Shell.StartSurfacesVector(builder, len(f_surfaces))
  for surface_offset in reversed(f_surfaces):
    builder.PrependUOffsetTRelative(surface_offset)
  f_surfaces_offset = builder.EndVector()

  Shell.Start(builder)
  Shell.AddSurfaces(builder, f_surfaces_offset)
  return Shell.End(builder)

def create_solid(builder, boundaries, semantics_values=None):
  f_shells = []
  if semantics_values:
    for shell, sem in zip(boundaries, semantics_values):
      f_shells.append(create_shell(builder, shell, sem))
  else:
    for shell in boundaries:
      f_shells.append(create_shell(builder, shell))
  
  Solid.StartShellsVector(builder, len(f_shells))
  for shell_offset in reversed(f_shells):
    builder.PrependUOffsetTRelative(shell_offset)
  f_shells_offset = builder.EndVector()
    
  Solid.Start(builder)
  Solid.AddShells(builder, f_shells_offset)
  return Solid.End(builder)

def create_polysolid(builder, boundaries, semantics_values=None):
  f_solids = []
  if semantics_values:
    for solid, sem in zip(geom["boundaries"], semantics_values):
      f_solids.append(create_solid(builder, solid, sem))
  else:
    for solid in geom["boundaries"]:
      f_solids.append(create_solid(builder, solid))

  # here it doesn't matter if it's MultiSolid or CompositeSolid, under the hood they are the same
  MultiSolid.StartSolidsVector(builder, len(f_solids))
  for solid_offset in reversed(f_solids):
    builder.PrependUOffsetTRelative(solid_offset)
  return builder.EndVector()

def create_polysurface(builder, boundaries, semantics_values=None):
  f_surfaces = []
  if semantics_values:
    for surface, sem in zip(boundaries, semantics_values):
      f_surfaces.append(create_surface(builder, surface, sem))
  else:
    for surface in boundaries:
      f_surfaces.append(create_surface(builder, surface))

  # here it doesn't matter if it's MultiSurface or CompositeSurface, under the hood they are the same
  MultiSurface.StartSurfacesVector(builder, len(f_surfaces))
  for surface_offset in reversed(f_surfaces):
    builder.PrependUOffsetTRelative(surface_offset)
  return builder.EndVector()

def create_feature(cj_feature, schema_encoder=None):
  def create_object(builder, cj_id, cj_object, schema_encoder):

    def create_geometry(builder, geom):
      f_lod = builder.CreateString(geom["lod"])

      semantic_values = None
      if "semantics" in geom:
        semantics = geom["semantics"]
        # TODO add semantics
        f_semantics_offsets = []
        if "surfaces" in semantics and "values" in semantics:
          for surface in semantics["surfaces"]:
            f_attributes_offset = builder.CreateByteVector( schema_encoder.encode_values(surface, exclude=["type"]) )
            SemanticObject.Start(builder)
            SemanticObject.SemanticObjectAddType(builder, get_attribute_by_name(SemanticSurfaceType, surface["type"]))
            SemanticObject.SemanticObjectAddAttributes(builder, f_attributes_offset)
            f_semantics_offsets.append(SemanticObject.End(builder))

          Geometry.StartSemanticsObjectsVector(builder, len(f_semantics_offsets))
          for offset in reversed(f_semantics_offsets):
            builder.PrependUOffsetTRelative(offset)
          f_semantics = builder.EndVector()
          semantic_values = semantics["values"]

        else:
          raise Exception("Semantics must have surfaces and values")

      # Create the boundaries field
      f_boundaries_offset = None
      if geom["type"] == "Solid":
        f_boundaries_offset = create_solid(builder, geom["boundaries"], semantic_values)

      elif geom["type"] == "MultiSurface" or geom["type"] == "CompositeSurface":
        f_boundaries_offset = create_polysurface(builder, geom["boundaries"], semantic_values)

      elif geom["type"] == "MultiSolid" or geom["type"] == "CompositeSolid":
        f_boundaries_offset = create_polysolid(builder, geom["boundaries"], semantic_values)

      elif geom["type"] == "MultiLineString":
        f_boundaries_offset = create_multilinestring(builder, geom["boundaries"], semantic_values)

      elif geom["type"] == "MultiPoint":
        f_boundaries_offset = create_multipoint(builder, geom["boundaries"], semantic_values)
      else:
        raise Exception("Geometry type not supported")
      
      Geometry.Start(builder)
      Geometry.GeometryAddLod(builder, f_lod)
      if semantic_values:
          Geometry.GeometryAddSemanticsObjects(builder, f_semantics)
      Geometry.GeometryAddBoundaries(builder, f_boundaries_offset)
      Geometry.GeometryAddBoundariesType(builder, get_attribute_by_name(Boundaries.Boundaries, geom["type"]))
      return Geometry.End(builder)

    has_children = "children" in cj_object
    has_parents = "parents" in cj_object
    has_attributes = "attributes" in cj_object
    has_geometry = "geometry" in cj_object

    f_id = builder.CreateString(cj_id)

    # create attributes
    if has_attributes and schema_encoder:
      # iterate of object attributes and build a binary buffer; the attribute values encoded back to back, each preceded by a column index
      buf_attributes = schema_encoder.encode_values(cj_object["attributes"])
      f_attributes_offset = builder.CreateByteVector(buf_attributes)

    # create parent string
    if has_parents:
      f_parents = []
      for parent in reversed(cj_object["parents"]):  # FlatBuffers requires reverse order when creating vectors
        f_parents.append(builder.CreateString(parent))

      CityObject.StartParentsVector(builder, len(f_parents))
      for parent in f_parents:
        builder.PrependUOffsetTRelative(parent)
      f_parents_offset = builder.EndVector()

    # create children strings vector
    if has_children:
      f_children = []
      for child in reversed(cj_object["children"]):  # FlatBuffers requires reverse order when creating vectors
        f_children.append(builder.CreateString(child))

      CityObject.StartChildrenVector(builder, len(f_children))
      for child in f_children:
        builder.PrependUOffsetTRelative(child)
      f_children_offset = builder.EndVector()

    # create geometries
    if has_geometry:
      f_geoms = []
      for geom in cj_object["geometry"]:
        if geom["type"] == "GeometryInstance":
          raise Exception("GeometryInstance is not supported at the moment")
        f_geoms.append(create_geometry(builder, geom))

      # Create the geometries vector
      CityObject.StartGeometryVector(builder, len(cj_object["geometry"]))
      for geom in reversed(f_geoms):  # FlatBuffers requires reverse order when creating vectors
        builder.PrependUOffsetTRelative(geom)
      f_geometries_offset = builder.EndVector()
    
    CityObject.Start(builder)
    # type
    CityObject.AddType(builder, get_attribute_by_name(CityObjectType, cj_object["type"]))
    # id
    CityObject.AddId(builder, f_id)

    # attributes, columns
    if has_attributes:
      CityObject.AddAttributes(builder, f_attributes_offset)

    # Geometries
    if has_geometry:
      CityObject.AddGeometry(builder, f_geometries_offset)

    # children
    if has_children:
      CityObject.AddChildren(builder, f_children_offset)

    # parent
    if has_parents:
      CityObject.AddParents(builder, f_parents_offset)

    return CityObject.End(builder)

  builder = flatbuffers.Builder(1024)

  f_id = builder.CreateString(cj_feature["id"])
  
  # should check if type is CityJSONFeature

  CityFBFeature.StartVerticesVector(builder, len(cj_feature["vertices"]))
  for v in reversed(cj_feature["vertices"]):  # FlatBuffers requires reverse order when creating vectors
      CreateVertex(builder, v[0], v[1], v[2])
  f_vertices_offset = builder.EndVector()

  f_object_offsets = []
  for (cj_id, cj_object) in cj_feature["CityObjects"].items():
    f_object_offsets.append(create_object(builder, cj_id, cj_object, schema_encoder))
  
  CityFBFeature.StartObjectsVector(builder, len(cj_feature["CityObjects"]))
  for offset in reversed(f_object_offsets):  # FlatBuffers requires reverse order when creating vectors
    builder.PrependUOffsetTRelative(offset)
  f_objects_offset = builder.EndVector()

  f = CityFBFeature.Start(builder)

  CityFBFeature.AddId(builder, f_id)
  CityFBFeature.AddVertices(builder, f_vertices_offset)
  CityFBFeature.AddObjects(builder, f_objects_offset)

  f = CityFBFeature.End(builder)
  builder.Finish(f)

  return builder.Output()

def create_header(cj_metadata, geographical_extent, features_count=3, schema_encoder=None):
  # Create a FlatBuffer builder
  builder = flatbuffers.Builder(1024)

  # Create the name string in the buffer
  # name = builder.CreateString("fcb_header_test")

  # Create the transform object in the buffer
  ts = cj_metadata['transform']['scale']
  tt = cj_metadata['transform']['translate']

  # Create the CRS table in the buffer
  crs_offset = None
  if 'metadata' in cj_metadata:
    if 'referenceSystem' in cj_metadata['metadata']:
      cj_crs = cj_metadata['metadata']['referenceSystem']
      authority, version, code = cj_crs.split('/')[-3:]
  
      authority_cfb = builder.CreateString(authority)

      crs = Crs.CrsStart(builder)
      Crs.CrsAddAuthority(builder, authority_cfb)
      Crs.CrsAddVersion(builder, int(version))
      Crs.CrsAddCode(builder, int(code))
      crs_offset = Crs.CrsEnd(builder)

  fb_columns = []
  for key, _ in schema_encoder.schema.items():
    f_name = builder.CreateString(key)
    # f_title = builder.CreateString(key)
    # f_description = builder.CreateString(key)
    # f_metadata = builder.CreateString(key)

    Column.Start(builder)
    Column.AddName(builder, f_name)
    f_type = schema_encoder.get_cb_column_type(key)
    Column.AddType(builder, f_type)
    # Column.AddTitle(builder, f_title)
    # Column.AddDescription(builder, f_description)
    # Column.AddNullable(builder, True)
    # Column.AddUnique(builder, False)
    # Column.AddPrimaryKey(builder, False)
    # Column.AddMetadata(builder, f_metadata)
    fb_columns.append(Column.End(builder))

  Header.StartColumnsVector(builder, len(fb_columns))
  for column_offset in reversed(fb_columns):
    builder.PrependUOffsetTRelative(column_offset)
  f_columns_offset = builder.EndVector()

  Header.HeaderStart(builder)
  # Header.AddName(builder, name)
  Header.AddFeaturesCount(builder, features_count)
  Header.HeaderAddTransform(builder, CreateTransform(builder, ts[0], ts[1], ts[2], tt[0], tt[1], tt[2]))
  if crs_offset:
    Header.HeaderAddCrs(builder, crs_offset)
  else:
    logging.warning("No CRS found in input metadata")
  Header.HeaderAddColumns(builder, f_columns_offset)
  gmin, gmax = geographical_extent
  Header.HeaderAddGeographicalExtent(builder, CreateGeographicalExtent(builder, gmin[0], gmin[1], gmin[2], gmax[0], gmax[1], gmax[2]))

  header = Header.HeaderEnd(builder)
  builder.Finish(header)

  return builder.Output()

def convert_cjseq2cb(cjseq_path, cb_path, pretyped_attributes={}):
  cj_features = []
  with open(cjseq_path, "r") as fo:
    cj_metadata = json.loads(fo.readline())
    for feature_str in fo:
        cj_features.append(json.loads(feature_str))

  schema_encoder = AttributeSchemaEncoder(pretyped_attributes)

  # scan attributes and geographical extents
  global_extent = np.ndarray((2, 3), dtype=np.float64)
  get_extent_from_features = True
  if "metadata" in cj_metadata:
    if "geographicalExtent" in cj_metadata["metadata"]:
      global_extent[0] = cj_metadata["metadata"]["geographicalExtent"][0:3]
      global_extent[1] = cj_metadata["metadata"]["geographicalExtent"][3:6]
      get_extent_from_features = False
    else:
      global_extent[0] = np.inf
      global_extent[1] = -np.inf
  for cj_feature in cj_features:
    for cj_object in cj_feature["CityObjects"].values():
      if get_extent_from_features:
        if "geographicalExtent" in cj_object:
          fext = np.ndarray((2, 3), dtype=np.float64)
          fext[0] = cj_object["geographicalExtent"][0:3]
          fext[1] = cj_object["geographicalExtent"][3:6]
          global_extent[0] = np.minimum(global_extent[0], fext[0])
          global_extent[1] = np.maximum(global_extent[1], fext[1])

      if "attributes" in cj_object:
        schema_encoder.add(cj_object["attributes"])

      if "geometry" in cj_object:
        for geom in cj_object["geometry"]:
          if "semantics" in geom:
            for surface in geom["semantics"]["surfaces"]:
                schema_encoder.add(surface, exclude=["type"])

  print("Using schema:")
  for name, value in schema_encoder.schema.items():
    print(f"\t{name}, {value.type}")

  fb_features = []
  for cj_feature in cj_features:
    fb_features.append(create_feature(cj_feature, schema_encoder))

  # Open a file in binary write mode
  with open(cb_path, 'wb') as file:
    # Write the byte data to the file
    file.write(create_magic_bytes(0,1))
    header_buf = create_header(cj_metadata, geographical_extent=global_extent, features_count=len(fb_features), schema_encoder=schema_encoder)
    file.write(len(header_buf).to_bytes(4, byteorder='little', signed=False))
    file.write(header_buf)
    for fb_feature in fb_features:
      file.write(len(fb_feature).to_bytes(4, byteorder='little', signed=False))
      file.write(fb_feature)

def print_cb(cb_path):
  # Define the number of bytes for the magic number
  MAGIC_NUMBER_SIZE = 6

  # Open the file and check if we can read the data
  with open(cb_path, 'rb') as f:
      # Read the magic number
      magic_number = f.read(MAGIC_NUMBER_SIZE)

      if magic_number[:2] == b'CB' and magic_number[3:5] == b'CB':
          print("Magic number is valid")
          print("Major version:", magic_number[2])
          print("Minor version:", magic_number[5])
      
      # Read the rest of the file (the FlatBuffer data)
      header_length = f.read(4)
      header_length = struct.unpack('<I', header_length)[0]
      print("Header length:", header_length)

      header_buf = f.read(header_length)

      # Get a pointer to the root object inside the FlatBuffer
      header = Header.Header.GetRootAsHeader(header_buf, 0)

      # Access the data

      # Print schema
      schema_decoder = AttributeSchemaDecoder(header)
      print(schema_decoder.schema)

      # name = header.Name().decode('utf-8')

      # Print GeographicalExtent
      extent = header.GeographicalExtent()
      emin = Vector.Vector()
      emax = Vector.Vector()
      extent.Min(emin)
      extent.Max(emax)
      print(f"GeographicalExtent: {emin.X()}, {emin.Y()}, {emin.Z()} | {emax.X()}, {emax.Y()}, {emax.Z()}")

      # Print Transform
      transform = header.Transform()
      Scale = Vector.Vector()
      Translate = Vector.Vector()
      transform.Scale(Scale)
      transform.Translate(Translate)
      print(f"Transform: {Scale.X()}, {Scale.Y()}, {Scale.Z()} | {Translate.X()}, {Translate.Y()}, {Translate.Z()}")

      # Print feature count
      fcount = header.FeaturesCount()
      print(f"FeaturesCount: {fcount}")

      # Print Crs
      crs = header.Crs()
      print(f"CRS: {crs.Authority().decode('utf-8')}/{crs.Version()}/{crs.Code()}")

      for i in range(fcount):
        feature_length = f.read(4)
        feature_length = struct.unpack('<I', feature_length)[0]
        feature_buf = f.read(feature_length)
        feature = CityFBFeature.CityFBFeature.GetRootAsCityFBFeature(feature_buf, 0)
        print(f"Feature length: {feature_length} bytes")
        print(f"Feature id: {feature.Id().decode('utf-8')}")
        print(f"Vertex count: {feature.VerticesLength()}")
        # for i in range(feature.VerticesLength()):
        #   print(f"Vertex {i}: {feature.Vertices(i).X()}, {feature.Vertices(i).Y()}, {feature.Vertices(i).Z()}")

        for i in range(feature.ObjectsLength()):
          obj = feature.Objects(i)
          print(f"Object {i}: id={obj.Id().decode('utf-8')}, type={obj.Type()}")
          if not obj.AttributesIsNone():
            print("Attributes:", schema_decoder.decode_attributes(obj.AttributesAsNumpy()))

          for j in range(obj.GeometryLength()):
            geom = obj.Geometry(j)
            print(f"Geometry {j}: lod={geom.Lod()}, type={geom.BoundariesType()}")
            print(f"GeometryType: {geom.BoundariesType()}")
            if geom.BoundariesType() == Boundaries.Boundaries.Solid:
              # create Solid object
              solid = Solid.Solid()
              solid.Init(geom.Boundaries().Bytes, geom.Boundaries().Pos)
              for ii in range(solid.Shells(0).Surfaces(0).Rings(0).IndicesLength()):
                print(f"First ring indices: {solid.Shells(0).Surfaces(0).Rings(0).Indices(ii)}")
              
            for k in range(geom.SemanticsObjectsLength()):
              sem = geom.SemanticsObjects(k)
              print(f"SemanticObject {k}: type={sem.Type()}, attributes:", schema_decoder.decode_attributes(sem.AttributesAsNumpy()))

if __name__ == "__main__":
  arg = argparse.ArgumentParser(description='Convert CityJSON sequence to CityBuffer')
  arg.add_argument('cjseq', help='CityJSON sequence file')
  arg.add_argument('cb', help='CityBuffer file')
  arg.add_argument('--schema', help='Predifine attribute types, important in case type cannot be unambiguously inferred from the data', type=str)
  args = arg.parse_args()

  pretyped_attributes = {}
  if args.schema:
    type_map = {
      'str': str,
      'int': int,
      'float': float,
      'bool': bool,
      'json': dict,
      # Add other types as needed
    }
    for pair in args.schema.split(','):
      name, atype = pair.split(':')
      pretyped_attributes[name] = type_map[atype]
      
  convert_cjseq2cb(args.cjseq, args.cb, pretyped_attributes)
  # print_cb(args.cb)