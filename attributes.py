from CityBuf_.ColumnType import ColumnType
import struct
import logging
import json

class AttributeSchemaEncoder:
  class Column:

    def __init__(self, type, order, schema_id=0):
      self.order = order
      self.type = type
      self.schema_id = schema_id

  # schema = {(Schema_id, name): Column, ...}
  schema = {}
  pretyped_names = []

  def __init__(self, pretyped_attributes={}):
    self.set_pretyped_attributes(pretyped_attributes)
    
  def set_pretyped_attributes(self, pretyped_attributes={}, schema_id=0):
    for key, value in pretyped_attributes.items():
      self.schema[(schema_id,key)] = self.Column(value, len(self.schema), schema_id)
      self.pretyped_names = pretyped_attributes.keys()

  def add(self, attributes, schema_id=0, exclude=[]):
    for key, value in attributes.items():
      if key == "on_footprint_edge":
        pass
      if key in exclude:
        continue
      if key in self.pretyped_names:
        continue
      if (schema_id, key) not in self.schema:
        self.schema[(schema_id, key)] = self.Column(type(value), len(self.schema))
      else: # this key is already in the schema
        t_val = type(value)
        t_schema = self.schema[(schema_id, key)].type
        if t_val != t_schema:
          if t_schema == None:
            self.schema[(schema_id, key)] = self.Column(t_val, len(self.schema), schema_id)
          elif t_val == float and t_schema == int:
            self.schema[(schema_id, key)] = self.Column(float, len(self.schema), schema_id)
            logging.warning("Type mismatch for column " + (schema_id, key) + ". Overwriting schema type to float")
          elif t_val == int and t_schema == bool:
            self.schema[(schema_id, key)] = self.Column(int, len(self.schema), schema_id)
            logging.warning("Type mismatch for column " + (schema_id, key) + ". Overwriting schema type to int")
          elif t_val == str and t_schema == int:
            self.schema[(schema_id, key)] = self.Column(str, len(self.schema), schema_id)
            logging.warning("Type mismatch for column " + (schema_id, key) + ". Overwriting schema type to string")

  def get_cb_column_type(self, name, schema_id=0):
    if self.schema[(schema_id, name)].type == str:
      return ColumnType.String
    elif self.schema[(schema_id, name)].type == int:
      return ColumnType.Int
    elif self.schema[(schema_id, name)].type == float:
      return ColumnType.Float
    elif self.schema[(schema_id, name)].type == bool:
      return ColumnType.Bool
    elif self.schema[(schema_id, name)].type == dict:
      return ColumnType.Json
    elif self.schema[(schema_id, name)].type == type(None):
      logging.warning("Type not set for column " + name + ". Defaulting to string")
      return ColumnType.String
    else:
      raise Exception("Type not supported")
    
  def encode_value(self, name, value, schema_id=0):
    # handle null values by not writing anything
    if value == None:
      return b""
    
    format = "=H" # don't add padding, unsigned short (2 bytes) is the column index
    t_schema = self.schema[(schema_id, name)].type
    if t_schema == str:
      if name in self.pretyped_names and type(value) != str:
        value = str(value)
      format += "I" # string length
      format += str(len(value)) # string length
      format += "s" # string
    elif t_schema == int:
      format += "i"
      if name in self.pretyped_names and type(value) != int:
        value = int(value)
    elif t_schema == float:
      format += "f"
      if name in self.pretyped_names and type(value) != float:
        value = float(value)
    elif t_schema == bool:
      format += "?"
      if name in self.pretyped_names and type(value) != bool:
        value = bool(value)
    elif t_schema == dict:
      value = json.dumps(value, separators=(',', ':'))
      format += "I" # string length
      format += str(len(value)) # string length
      format += "s" # string
    else:
      raise Exception("Type not supported")
    
    if t_schema == str or t_schema == dict:
      return struct.pack(format, self.schema[(schema_id, name)].order, len(value), value.encode('utf-8'))
    else:
      return struct.pack(format, self.schema[(schema_id, name)].order, value)

  def encode_values(self, attributes, schema_id=0, exclude=[]):
    buf = struct.pack("=H", schema_id) # unsigned short (2 bytes) is the schema id
    for key, value in attributes.items():
      if key in exclude:
        continue
      buf += self.encode_value(key, value, schema_id)
    return buf

class AttributeSchemaDecoder:
  schema = {} # {index : (schema_id, name, type)}
  def __init__(self, cb_header):
    for ci in range(cb_header.ColumnsLength()):
      col = cb_header.Columns(ci)
      self.schema[ci] = (col.SchemaId(), col.Name().decode('utf-8'), col.Type())
  
  # buffer is retreived from the AttributesAsNumpy() method
  def decode_attributes(self, buffer, write_nulls=False):
    ib = 0
    attributes = {}
    schema_id = column_index = struct.unpack('H', buffer[ib:ib+2])[0]
    ib += 2
    while ib < len(buffer):
      column_index = struct.unpack('H', buffer[ib:ib+2])[0]
      ib += 2
      attr_type = self.schema[column_index][2]
      if attr_type == ColumnType.String:
        value_length = struct.unpack('I', buffer[ib:ib+4])[0]
        value = buffer[ib+4:ib+4+value_length].tobytes().decode('utf-8')
        ib += 4 + value_length
      elif attr_type == ColumnType.Int:
        value = struct.unpack('i', buffer[ib:ib+4])[0]
        ib += 4
      elif attr_type == ColumnType.Float:
        value = struct.unpack('f', buffer[ib:ib+4])[0]
        ib += 4
      elif attr_type == ColumnType.Bool:
        value = struct.unpack('?', buffer[ib:ib+1])[0]
        ib += 1
      elif attr_type == ColumnType.Json:
        value_length = struct.unpack('I', buffer[ib:ib+4])[0]
        value = json.loads(buffer[ib+4:ib+4+value_length].tobytes().decode('utf-8'))
        ib += 4 + value_length
      else:
        raise Exception("Type not supported")
      attributes[self.schema[column_index][1]] = value
        # raise Exception("Type not supported")
    
    # add null valued attributes that are defined for this schema_id
    if write_nulls:
      for ci in range(len(self.schema)):
        if self.schema[ci][0] == schema_id and self.schema[ci][1] not in attributes:
          attributes[self.schema[ci][1]] = None

    return attributes