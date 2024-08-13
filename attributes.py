from flatCitybuf.ColumnType import ColumnType
import struct

class AttributeSchemaEncoder:
  # schema = {"name": type, ...}
  schema = {}
  schema_order = {}

  def add(self, attributes):
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

  def get_cb_column_type(self, name):
    if self.schema[name] == str:
      return ColumnType.String
    elif self.schema[name] == int:
      return ColumnType.Int
    elif self.schema[name] == float:
      return ColumnType.Float
    elif self.schema[name] == bool:
      return ColumnType.Bool
    else:
      raise Exception("Type not supported")
    
  def encode_value(self, name, value):
    format = "=H" # don't add padding, unsigned short (2 bytes) is the column index
    if self.schema[name] == str:
      format += "I" # string length
      format += str(len(value)) # string length
      format += "s" # string
    elif self.schema[name] == int:
      format += "i"
    elif self.schema[name] == float:
      format += "f"
    elif self.schema[name] == bool:
      format += "?"
    else:
      raise Exception("Type not supported")
    
    if self.schema[name] == str:
      return struct.pack(format, self.schema_order[name], len(value), value.encode('utf-8'))
    else:
      return struct.pack(format, self.schema_order[name], value)

  def encode_values(self, attributes):
    buf = b""
    for key, value in attributes.items():
      buf += self.encode_value(key, value)
    return buf
    
  def finalise(self):
    self.schema_order = dict(zip(self.schema.keys(), range(len(self.schema.keys()))))

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