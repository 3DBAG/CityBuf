import json

from flatCitybuf import Header, CityFBFeature, CityObject, Crs, Geometry, Solid, Boundaries, Shell, Ring, Surface, MultiSurface, CompositeSurface, MultiSolid, CompositeSolid, SemanticObject, Column
from flatCitybuf.SemanticSurfaceType import SemanticSurfaceType
from flatCitybuf.CityObjectType import CityObjectType
from flatCitybuf.ColumnType import ColumnType
from flatCitybuf.Vertex import CreateVertex
from flatCitybuf.Transform import CreateTransform
import flatbuffers

import struct

def create_magic_bytes(major=0, minor=1):
  fcb = "FCB".encode('ascii')
  ma = major.to_bytes(1, byteorder='little')
  mi = minor.to_bytes(1, byteorder='little')

  # Convert ASCII string to bytes
  return fcb + ma + fcb + mi

def get_attribute_by_name(class_type, attribute_name):
    return getattr(class_type, attribute_name, None)

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
  
  # TODO add semantics

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

def create_feature(cj_feature):
  def create_object(builder, cj_id, cj_object):

    def create_geometry(builder, geom):
      f_lod = builder.CreateString(geom["lod"])

      semantic_values = None
      if "semantics" in geom:
        semantics = geom["semantics"]
        # TODO add semantics
        f_semantics_offsets = []
        if "surfaces" in semantics and "values" in semantics:
          for surface in semantics["surfaces"]:
            SemanticObject.Start(builder)
            SemanticObject.SemanticObjectAddType(builder, get_attribute_by_name(SemanticSurfaceType, surface["type"]))
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
        f_surfaces = []
        for surface in geom["boundaries"]:
          f_surfaces.append(create_surface(builder, surface, semantic_values))

        # here it doesn't matter if it's MultiSurface or CompositeSurface, under the hood they are the same
        MultiSurface.StartSurfacesVector(builder, len(f_surfaces))
        for surface_offset in reversed(f_surfaces):
          builder.PrependUOffsetTRelative(surface_offset)
        f_boundaries_offset = builder.EndVector()        

      elif geom["type"] == "MultiSolid" or geom["type"] == "CompositeSolid":
        f_solids = []
        for solid in geom["boundaries"]:
          f_solids.append(create_solid(builder, solid, semantic_values))

        # here it doesn't matter if it's MultiSolid or CompositeSolid, under the hood they are the same
        MultiSolid.StartSolidsVector(builder, len(f_solids))
        for solid_offset in reversed(f_solids):
          builder.PrependUOffsetTRelative(solid_offset)
        f_boundaries_offset = builder.EndVector()
      
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

    f_id = builder.CreateString(cj_id)

    # create attributes

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
    f_geoms = []
    for geom in cj_object["geometry"]:
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

    # Geometries
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
    f_object_offsets.append(create_object(builder, cj_id, cj_object))
  
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

def create_header(cj_metadata, geographicalExtent=[8.5, 9.2, 7.3, 6.8], features_count=3, schema_builder=None):
  # Create a FlatBuffer builder
  builder = flatbuffers.Builder(1024)

  # Create the name string in the buffer
  # name = builder.CreateString("fcb_header_test")

  # Create the transform object in the buffer
  ts = cj_metadata['transform']['scale']
  tt = cj_metadata['transform']['translate']

  # Create the CRS table in the buffer
  cj_crs = cj_metadata['metadata']['referenceSystem']
  authority, version, code = cj_crs.split('/')[-3:]
  
  authority_cfb = builder.CreateString(authority)

  crs = Crs.CrsStart(builder)
  Crs.CrsAddAuthority(builder, authority_cfb)
  Crs.CrsAddVersion(builder, int(version))
  Crs.CrsAddCode(builder, int(code))
  crs_offset = Crs.CrsEnd(builder)

  fb_columns = []
  for key, type in schema_builder.schema.items():
    f_name = builder.CreateString(key)
    # f_title = builder.CreateString(key)
    # f_description = builder.CreateString(key)
    # f_metadata = builder.CreateString(key)

    Column.Start(builder)
    Column.AddName(builder, f_name)
    if type == str:
      f_type = ColumnType.String
    elif type == int:
      f_type = ColumnType.Int
    elif type == float:
      f_type = ColumnType.Float
    elif type == bool:
      f_type = ColumnType.Bool
    else:
      raise Exception("Type not supported")
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
  Header.HeaderAddCrs(builder, crs_offset)
  Header.HeaderAddColumns(builder, f_columns_offset)

  header = Header.HeaderEnd(builder)
  builder.Finish(header)

  return builder.Output()

cj_metadata = json.load(open('data/metadata.json'))
cj_features = [json.load(open('data/503100000000296.city.jsonl'))]

class AttributeSchemaBuilder:
  # schema = {"name": type, ...}
  schema = {}
  schema_order = {}

  def scan(self, attributes):
    for key, value in attributes.items():
      if key not in self.schema:
        self.schema[key] = type(value)
      else:
        t_val = type(value)
        t_schema = type(self.schema[key])
        if t_val != t_schema:
          if t_schema == None:
            self.schema[key] = t_val
          if t_val == float and t_schema == int:
            self.schema[key] = float
          if t_val == int and t_schema == bool:
            self.schema[key] = int
  def finalise(self):
    self.schema_order = dict(zip(self.schema.keys(), range(len(self.schema.keys()))))

schema_builder = AttributeSchemaBuilder()

for cj_feature in cj_features:
  # scan attributes
  for cj_object in cj_feature["CityObjects"].values():
    if "attributes" in cj_object:
      schema_builder.scan(cj_object["attributes"])
schema_builder.finalise()

fb_features = []
for cj_feature in cj_features:
  fb_features.append(create_feature(cj_feature))

# Open a file in binary write mode
with open('file.cfb', 'wb') as file:
  # Write the byte data to the file
  file.write(create_magic_bytes(0,1))
  header_buf = create_header(cj_metadata, features_count=len(fb_features), schema_builder=schema_builder)
  file.write(len(header_buf).to_bytes(4, byteorder='little', signed=False))
  file.write(header_buf)
  for fb_feature in fb_features:
    file.write(len(fb_feature).to_bytes(4, byteorder='little', signed=False))
    file.write(fb_feature)

# Define the number of bytes for the magic number
MAGIC_NUMBER_SIZE = 8

# Open the file and check if we can read the data
with open('file.cfb', 'rb') as f:
    # Read the magic number
    magic_number = f.read(MAGIC_NUMBER_SIZE)

    if magic_number[:3] == b'FCB' and magic_number[4:7] == b'FCB':
        print("Magic number is valid")
        print("Major version:", magic_number[3])
        print("Minor version:", magic_number[7])
    
    # Read the rest of the file (the FlatBuffer data)
    header_length = f.read(4)
    header_length = struct.unpack('<I', header_length)[0]
    print("Header length:", header_length)

    header_buf = f.read(header_length)

    # Get a pointer to the root object inside the FlatBuffer
    header = Header.Header.GetRootAsHeader(header_buf, 0)

    # Access the data
    fcount = header.FeaturesCount()
    for column in range(header.ColumnsLength()):
      col = header.Columns(column)
      print(f"Column {column}: {col.Name().decode('utf-8')}, {col.Type()}")
    # name = header.Name().decode('utf-8')

    # # Access the envelope array
    # envelope = [header.Envelope(i) for i in range(header.EnvelopeLength())]

    # Print the data
    print(f"FeaturesCount: {fcount}")

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
        for j in range(obj.GeometryLength()):
          geom = obj.Geometry(j)
          print(f"Geometry {j}: lod={geom.Lod()}, type={geom.BoundariesType()}")
          for k in range(geom.SemanticsObjectsLength()):
            sem = geom.SemanticsObjects(k)
            print(f"SemanticObject {k}: type={sem.Type()}")