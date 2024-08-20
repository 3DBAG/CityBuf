from CityBuf_.ColumnType import ColumnType
import struct
import logging
import json
import numpy as np

class AttributeSchemaEncoder:
  class Column:
    type = None
    order = None

    def __init__(self, type, order):
      self.order = order
      self.type = type

  # schema = {"name": Column, ...}
  schema = {}
  pretyped_names = []

  def __init__(self, pretyped_attributes={}, write_nulls=False):
    self.write_nulls = write_nulls
    for key, value in pretyped_attributes.items():
      self.schema[key] = self.Column(value, len(self.schema))
      self.pretyped_names = pretyped_attributes.keys()

  def add(self, attributes, exclude=[]):
    for key, value in attributes.items():
      if key in exclude:
        continue
      if key in self.pretyped_names:
        continue
      if key not in self.schema:
        self.schema[key] = self.Column(type(value), len(self.schema))
      else:
        t_val = type(value)
        t_schema = self.schema[key].type
        if t_val != t_schema:
          if t_schema == None:
            self.schema[key] = self.Column(t_val, len(self.schema))
          elif t_val == float and t_schema == int:
            self.schema[key] = self.Column(float, len(self.schema))
            logging.warning("Type mismatch for column " + key + ". Overwriting schema type to float")
          elif t_val == int and t_schema == bool:
            self.schema[key] = self.Column(int, len(self.schema))
            logging.warning("Type mismatch for column " + key + ". Overwriting schema type to int")
          elif t_val == str and t_schema == int:
            self.schema[key] = self.Column(str, len(self.schema))
            logging.warning("Type mismatch for column " + key + ". Overwriting schema type to string")

  def get_cb_column_type(self, name):
    if self.schema[name].type == str:
      return ColumnType.String
    elif self.schema[name].type == int:
      return ColumnType.Int
    elif self.schema[name].type == float:
      return ColumnType.Float
    elif self.schema[name].type == bool:
      return ColumnType.Bool
    elif self.schema[name].type == dict:
      return ColumnType.Json
    elif self.schema[name].type == type(None):
      logging.warning("Type not set for column " + name + ". Defaulting to string")
      return ColumnType.String
    else:
      raise Exception("Type not supported")
    
  def encode_value(self, name, value, write_null=False):
    # handle null values by not writing anything
    if value == None:
      if write_null:
        return struct.pack("=HH", np.iinfo(np.uint16).max, self.schema[name].order)
      else:
        return b""
    
    format = "=H" # don't add padding, unsigned short (2 bytes) is the column index
    if self.schema[name].type == str:
      if name in self.pretyped_names and type(value) != str:
        value = str(value)
      format += "I" # string length
      format += str(len(value)) # string length
      format += "s" # string
    elif self.schema[name].type == int:
      format += "i"
      if name in self.pretyped_names and type(value) != int:
        value = int(value)
    elif self.schema[name].type == float:
      format += "f"
      if name in self.pretyped_names and type(value) != float:
        value = float(value)
    elif self.schema[name].type == bool:
      format += "?"
      if name in self.pretyped_names and type(value) != bool:
        value = bool(value)
    elif self.schema[name].type == dict:
      value = json.dumps(value, separators=(',', ':'))
      format += "I" # string length
      format += str(len(value)) # string length
      format += "s" # string
    else:
      raise Exception("Type not supported")
    
    if self.schema[name].type == str or self.schema[name].type == dict:
      return struct.pack(format, self.schema[name].order, len(value), value.encode('utf-8'))
    else:
      return struct.pack(format, self.schema[name].order, value)

  def encode_values(self, attributes, exclude=[]):
    buf = b""
    for key, value in attributes.items():
      if key in exclude:
        continue
      buf += self.encode_value(key, value, self.write_nulls)
    return buf

class AttributeSchemaDecoder:
  schema = {}
  def __init__(self, cb_header):
    for ci in range(cb_header.ColumnsLength()):
      col = cb_header.Columns(ci)
      self.schema[ci] = (col.Name().decode('utf-8'), col.Type())
  
  # buffer is retreived from the AttributesAsNumpy() method
  def decode_attributes(self, buffer):
    ib = 0
    attributes = {}
    while ib < len(buffer):
      column_index = struct.unpack('H', buffer[ib:ib+2])[0]
      ib += 2
      # check if this is a null value for some field
      if column_index == np.iinfo(np.uint16).max:
        column_index = struct.unpack('H', buffer[ib:ib+2])[0]
        ib += 2
        value = None
      elif column_index >= len(self.schema):
        raise Exception("Column index out of bounds")
      else:
        attr_type = self.schema[column_index][1]
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
      attributes[self.schema[column_index][0]] = value
        # raise Exception("Type not supported")

    return attributes