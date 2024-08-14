from flatCitybuf.ColumnType import ColumnType
import struct
import logging

class AttributeSchemaEncoder:
  class Column:
    type = None
    order = None

    def __init__(self, type, order):
      self.order = order
      self.type = type

  # schema = {"name": Column, ...}
  schema = {}

  def add(self, attributes, exclude=[]):
    for key, value in attributes.items():
      if key in exclude:
        continue
      if key not in self.schema:
        self.schema[key] = self.Column(type(value), len(self.schema))
      else:
        t_val = type(value)
        t_schema = self.schema[key].type
        if t_val != t_schema:
          if t_schema == None:
            self.schema[key] = self.Column(t_val, len(self.schema))
          if t_val == float and t_schema == int:
            self.schema[key] = self.Column(float, len(self.schema))
          if t_val == int and t_schema == bool:
            self.schema[key] = self.Column(int, len(self.schema))

  def get_cb_column_type(self, name):
    if self.schema[name].type == str:
      return ColumnType.String
    elif self.schema[name].type == int:
      return ColumnType.Int
    elif self.schema[name].type == float:
      return ColumnType.Float
    elif self.schema[name].type == bool:
      return ColumnType.Bool
    elif self.schema[name].type == type(None):
      logging.warning("Type not set for column " + name + ". Defaulting to string")
      return ColumnType.String
    else:
      raise Exception("Type not supported")
    
  def encode_value(self, name, value):
    # handle null values by not writing anything
    if value == None:
      return b""
    
    format = "=H" # don't add padding, unsigned short (2 bytes) is the column index
    if self.schema[name].type == str:
      format += "I" # string length
      format += str(len(value)) # string length
      format += "s" # string
    elif self.schema[name].type == int:
      format += "i"
    elif self.schema[name].type == float:
      format += "f"
    elif self.schema[name].type == bool:
      format += "?"
    else:
      raise Exception("Type not supported")
    
    if self.schema[name].type == str:
      return struct.pack(format, self.schema[name].order, len(value), value.encode('utf-8'))
    else:
      return struct.pack(format, self.schema[name].order, value)

  def encode_values(self, attributes, exclude=[]):
    buf = b""
    for key, value in attributes.items():
      if key in exclude:
        continue
      buf += self.encode_value(key, value)
    return buf

class AttributeSchemaDecoder:
  schema = {}
  def __init__(self, cb_header):
    for ci in range(cb_header.ColumnsLength()):
      col = cb_header.Columns(ci)
      self.schema[ci] = (col.Name().decode('utf-8'), col.Type())

  def decode_value(self, column_index, value):
    name, type = self.schema[column_index]
    if type == ColumnType.String:
      return value.decode('utf-8')
    else:
      return value
      
  def decode_attributes(self, buffer):
    ib = 0
    attributes = {}
    while ib < len(buffer):
      column_index = struct.unpack('H', buffer[ib:ib+2])[0]
      ib += 2
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
      else:
        raise Exception("Type not supported")
      attributes[self.schema[column_index][0]] = value
        # raise Exception("Type not supported")

    return attributes