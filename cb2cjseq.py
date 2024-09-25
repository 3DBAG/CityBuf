# Copyright (c) 2024 TU Delft 3D geoinformation group, Ravi Peters (3DGI), Balazs Dukai (3DGI)
#
# This file is part of CityBuf
#
# CityBuf was created as part of the 3DBAG project by the TU Delft 3D geoinformation group (3d.bk.tudelf.nl) and 3DGI (3dgi.nl)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author(s): 
# Ravi Peters

import argparse, json
from CityBufReader import CityBufReader
from CityBuf_.GeometryType import GeometryType
from CityBuf_.CityObjectType import CityObjectType
from CityBuf_.SemanticSurfaceType import SemanticSurfaceType
from CityBuf_ import Vector

from attributes import AttributeSchemaDecoder
from geometry import GeometryDecoder

def generate_cityjson_root_object(header):
  transform = header.Transform()
  Scale = Vector.Vector()
  Translate = Vector.Vector()
  transform.Scale(Scale)
  transform.Translate(Translate)

  ge = header.GeographicalExtent()
  ge_min = Vector.Vector()
  ge_max = Vector.Vector()
  ge.Min(ge_min)
  ge.Max(ge_max)
  
  cj = {
    "type": "CityJSON",
    "version": "2.0",
    "CityObjects": {},
    "vertices": [],
    "transform": {
      "scale": [Scale.X(), Scale.Y(), Scale.Z()],
      "translate": [Translate.X(), Translate.Y(), Translate.Z()]
    },
    "metadata": {
      "geographicalExtent": [ge_min.X(), ge_min.Y(), ge_min.Z(), ge_max.X(), ge_max.Y(), ge_max.Z()]
    }
  }
  crs = header.ReferenceSystem()
  if crs:
    crs_auth = crs.Authority().decode("utf-8")
    crs_version = crs.Version()
    crs_code = crs.Code()
    crs_str = f"https://www.opengis.net/def/crs/{crs_auth}/{crs_version}/{crs_code}"
    cj["metadata"]["referenceSystem"] = crs_str
  return cj

def generate_cityjson_feature(feature, schema_decoder):
  def get_class_attribute_name_by_value(cls, value):
    for attr_name, attr_value in cls.__dict__.items():
      if attr_value == value:
        return attr_name
    return None
  
  cjf = {
     "id": feature.Id().decode("utf-8"),
     "type": "CityJSONFeature",
     "CityObjects": {},
     "vertices": []
  }
  
  for i in range(feature.VerticesLength()):
    vert = feature.Vertices(i)
    cjf["vertices"].append([vert.X(), vert.Y(), vert.Z()])
  
  for i in range(feature.ObjectsLength()):
    obj = feature.Objects(i)

    cjo_type = get_class_attribute_name_by_value(CityObjectType, obj.Type())

    cjo = {
      "type": cjo_type,
      "geometry": []
    }

    if not obj.AttributesIsNone():
      cjo["attributes"] = schema_decoder.decode_attributes(obj.AttributesAsNumpy())

    if not obj.ChildrenIsNone():
      cjo["children"] = []
      for j in range(obj.ChildrenLength()):
        cjo["children"].append(obj.Children(j).decode("utf-8"))

    if not obj.ChildrenRolesIsNone():
      cjo["children_roles"] = []
      for j in range(obj.ChildrenRolesLength()):
        cjo["children_roles"].append(obj.ChildrenRoles(j).decode("utf-8"))

    if not obj.ParentsIsNone():
      cjo["parents"] = []
      for j in range(obj.ParentsLength()):
        cjo["parents"].append(obj.Parents(j).decode("utf-8"))

    # TODO: Colunmns

    if obj.GeographicalExtent():
      ge = obj.GeographicalExtent()
      ge_min = Vector.Vector()
      ge_max = Vector.Vector()
      ge.Min(ge_min)
      ge.Max(ge_max)
      cjo["geographicalExtent"] = [ge_min.X(), ge_min.Y(), ge_min.Z(), ge_max.X(), ge_max.Y(), ge_max.Z()]

    for j in range(obj.GeometryLength()):
      geom = obj.Geometry(j)
      boundaries = None if geom.BoundariesIsNone() else geom.BoundariesAsNumpy().tolist()
      strings = None if geom.StringsIsNone() else geom.StringsAsNumpy().tolist()
      surfaces = None if geom.SurfacesIsNone() else geom.SurfacesAsNumpy().tolist()
      shells = None if geom.ShellsIsNone() else geom.ShellsAsNumpy().tolist()
      solids = None if geom.SolidsIsNone() else geom.SolidsAsNumpy().tolist()
      geom_encoder = GeometryDecoder(
                  boundaries,
                  strings,
                  surfaces,
                  shells,
                  solids
                )
      cjg = {
        "type": get_class_attribute_name_by_value(GeometryType, geom.Type()),
      }
      if not geom.SemanticsIsNone():
        geom_encoder.set_semantics(geom.SemanticsAsNumpy().tolist())
        cjg["semantics"] = {
          "surfaces": [],
          "values": geom_encoder.decode_semantics(geom.Type())
        }
        for k in range(geom.SemanticsObjectsLength()):
          sem = geom.SemanticsObjects(k)
          cjso = {   
            "type": get_class_attribute_name_by_value(SemanticSurfaceType, sem.Type())
          }
          if not sem.AttributesIsNone():
            cjso |= schema_decoder.decode_attributes(sem.AttributesAsNumpy())
          if not sem.Parent() == None:
            cjso["parent"] = sem.Parent()
          if not sem.ChildrenIsNone():
            cjso["children"] = []
            for l in range(sem.ChildrenLength()):
              cjso["children"].append(sem.Children(l))
          cjg["semantics"]["surfaces"].append(cjso)
      if geom.Lod():
        cjg["lod"] = geom.Lod().decode("utf-8")
      
      cjg["boundaries"] = geom_encoder.decode(geom.Type())

      cjo["geometry"].append(cjg)
      
    cjo_id = obj.Id().decode("utf-8")
    cjf["CityObjects"][cjo_id] = cjo
  return cjf

def convert_cb2cjseq(cb_path, cjseq_path):
  with open(cb_path, "rb") as cb_file:
    with open(cjseq_path, "w") as cjseq_file:
      reader = CityBufReader(cb_file)

      cj = generate_cityjson_root_object(reader.header)
      json.dump(cj, cjseq_file)
      cjseq_file.write('\n')

      schema_decoder = AttributeSchemaDecoder(reader.header)
      for feature in reader.features():
        json.dump(generate_cityjson_feature(feature, schema_decoder), cjseq_file)
        cjseq_file.write('\n')

if __name__ == "__main__":
  arg = argparse.ArgumentParser(description='Convert CityJSON sequence to CityBuffer')
  arg.add_argument('cb', help='CityBuffer file')
  arg.add_argument('cjseq', help='CityJSON sequence file')
  args = arg.parse_args()
  convert_cb2cjseq(args.cb, args.cjseq)