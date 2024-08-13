# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatCitybuf

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
from flatCitybuf.Surface import Surface
from typing import Optional
np = import_numpy()

class MultiSurface(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset: int = 0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = MultiSurface()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsMultiSurface(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # MultiSurface
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # MultiSurface
    def Surfaces(self, j: int) -> Optional[Surface]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            obj = Surface()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # MultiSurface
    def SurfacesLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # MultiSurface
    def SurfacesIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

def MultiSurfaceStart(builder: flatbuffers.Builder):
    builder.StartObject(1)

def Start(builder: flatbuffers.Builder):
    MultiSurfaceStart(builder)

def MultiSurfaceAddSurfaces(builder: flatbuffers.Builder, surfaces: int):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(surfaces), 0)

def AddSurfaces(builder: flatbuffers.Builder, surfaces: int):
    MultiSurfaceAddSurfaces(builder, surfaces)

def MultiSurfaceStartSurfacesVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartSurfacesVector(builder, numElems: int) -> int:
    return MultiSurfaceStartSurfacesVector(builder, numElems)

def MultiSurfaceEnd(builder: flatbuffers.Builder) -> int:
    return builder.EndObject()

def End(builder: flatbuffers.Builder) -> int:
    return MultiSurfaceEnd(builder)
