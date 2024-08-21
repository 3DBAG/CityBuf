from CityBuf_.GeometryType import GeometryType

class GeometryEncoder:
  def __init__(self):
    self.solids = []
    self.shells = []
    self.surfaces = []
    self.strings = [] # Rings or LineStrings
    self.indices = []
    self.semantic_values = []

  def encode(self, bounds):
    if type(bounds[0]) == list:
      for b in bounds:
        d = self.encode(b)
      l = len(bounds)
      if d == 1:
        self.surfaces.append(l)
      elif d == 2:
        self.shells.append(l)
      elif d == 3:
        self.solids.append(l)
      return d+1
    else:
      self.indices += bounds
      self.strings.append(len(bounds))
      return 1 # depth
    
  def encode_semantics(self, semantic_values):
    if type(semantic_values[0]) == list:
      for sem in semantic_values:
        return self.encode_semantics(sem)
    else:
      self.semantic_values += semantic_values
      return

# reverses the operation of the encoder
class GeometryDecoder:

  def __init__(self, indices, strings, surfaces, shells, solids):
    self.part_lists = {
      0: indices,
      1: strings,
      2: surfaces,
      3: shells,
      4: solids
    }

  def reset_starts(self):
    self.starts = {
      0: 0,
      1: 0,
      2: 0,
      3: 0,
      4: 0
    }

  def set_semantics(self, semantic_indices):
    self.semantic_indices = semantic_indices

  def decode_(self, d, start=None, n=None):
    # initial call
    if start == None or n == None:
      # we are dealing with a nested boundary list
      if d > 0:
        parts = []
        for gn in self.part_lists[d]:
          parts.append(self.decode_(d-1, self.starts[d], gn))
          self.starts[d] += gn
        return parts
      elif d == 0:
        # we are dealing with multi points
        return self.part_lists[d]
    
    # subsequent recursive calls:
    elif d == 0:
      return self.part_lists[d][start:start+n]
    else:
      parts = []
      for gn in self.part_lists[d][start:start+n]:
        parts.append(self.decode_(d-1, self.starts[d], gn))
        self.starts[d] += gn
      return parts
  
  def decode(self, geometry_type):
    self.reset_starts()
    if geometry_type == GeometryType.MultiSolid or \
       geometry_type == GeometryType.CompositeSolid:
      return self.decode_(4)
    elif geometry_type == GeometryType.Solid:
      return self.decode_(3)
    elif geometry_type == GeometryType.MultiSurface or \
         geometry_type == GeometryType.CompositeSurface:
      return self.decode_(2)
    elif geometry_type == GeometryType.MultiLineString:
      return self.decode_(1)
    elif geometry_type == GeometryType.MultiPoint:
      return self.decode_(0)
    
  def decode_semantics_(self, d, start=None, n=None):
    # initial call
    if start == None or n == None:
      # we are dealing with a nested boundary list
      if d > 2:
        parts = []
        for gn in self.part_lists[d]:
          parts.append(self.decode_semantics_(d-1, self.starts[d], gn))
          self.starts[d] += gn
        return parts
      elif d <= 2:
        return self.semantic_indices
        
    # subsequent recursive calls:
    if d <= 2: # semantics nesting is 2 levels less deep than geometry nesting
      return self.semantic_indices[start:start+n]
    else:
      parts = []
      for gn in self.part_lists[d][start:start+n]:
        parts.append(self.decode_semantics_(d-1, self.starts[d], gn))
        self.starts[d] += gn
      return parts
    
  def decode_semantics(self, geometry_type):
    self.reset_starts()
    if geometry_type == GeometryType.MultiSolid or \
       geometry_type == GeometryType.CompositeSolid:
      return self.decode_semantics_(4)
    elif geometry_type == GeometryType.Solid:
      return self.decode_semantics_(3)
    elif geometry_type == GeometryType.MultiSurface or \
         geometry_type == GeometryType.CompositeSurface or \
         geometry_type == GeometryType.MultiLineString or \
         geometry_type == GeometryType.MultiPoint:
      return self.semantic_indices