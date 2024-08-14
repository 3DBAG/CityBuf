import struct

from flatCitybuf import \
  Header, \
  CityFBFeature

class CityBufReader:
  MAGIC_NUMBER_SIZE = 6

  def __init__(self, file):
    self.f = file
    self.f.seek(0)
    self.read_magic_number()
    self.pos_header = 6
    self.read_header()
    self.pos_data = self.f.tell()
  
  def read_magic_number(self):
    self.f.seek(0)
    magic_number = self.f.read(self.MAGIC_NUMBER_SIZE)

    if magic_number[:2] == b'CB' and magic_number[3:5] == b'CB':
      self.version_major = magic_number[2]
      self.version_minor = magic_number[5]
    else:
      raise Exception('Invalid magic number')

  def read_header(self):
    self.f.seek(self.pos_header)
    header_length = struct.unpack('<I', self.f.read(4))[0]
    # print(f"Header size: {header_length} bytes")

    header_buf = self.f.read(header_length)

    # Get a pointer to the root object inside the FlatBuffer
    self.header = Header.Header.GetRootAsHeader(header_buf, 0)

  # iterator over the features
  def features(self):
    self.f.seek(self.pos_data)
    for i in range(self.header.FeaturesCount()):
      feature_length = struct.unpack('<I', self.f.read(4))[0]

      feature_buf = self.f.read(feature_length)
      feature = CityFBFeature.CityFBFeature.GetRootAsCityFBFeature(feature_buf, 0)
      yield feature
