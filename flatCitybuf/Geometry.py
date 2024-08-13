# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatCitybuf

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
from flatCitybuf.SemanticObject import SemanticObject
from flatbuffers.table import Table
from typing import Optional
np = import_numpy()

class Geometry(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset: int = 0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Geometry()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsGeometry(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Geometry
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Geometry
    def Lod(self) -> Optional[str]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Geometry
    def BoundariesType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Geometry
    def Boundaries(self) -> Optional[flatbuffers.table.Table]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

    # Geometry
    def SemanticsObjects(self, j: int) -> Optional[SemanticObject]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            obj = SemanticObject()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Geometry
    def SemanticsObjectsLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Geometry
    def SemanticsObjectsIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        return o == 0

def GeometryStart(builder: flatbuffers.Builder):
    builder.StartObject(4)

def Start(builder: flatbuffers.Builder):
    GeometryStart(builder)

def GeometryAddLod(builder: flatbuffers.Builder, lod: int):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(lod), 0)

def AddLod(builder: flatbuffers.Builder, lod: int):
    GeometryAddLod(builder, lod)

def GeometryAddBoundariesType(builder: flatbuffers.Builder, boundariesType: int):
    builder.PrependUint8Slot(1, boundariesType, 0)

def AddBoundariesType(builder: flatbuffers.Builder, boundariesType: int):
    GeometryAddBoundariesType(builder, boundariesType)

def GeometryAddBoundaries(builder: flatbuffers.Builder, boundaries: int):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(boundaries), 0)

def AddBoundaries(builder: flatbuffers.Builder, boundaries: int):
    GeometryAddBoundaries(builder, boundaries)

def GeometryAddSemanticsObjects(builder: flatbuffers.Builder, semanticsObjects: int):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(semanticsObjects), 0)

def AddSemanticsObjects(builder: flatbuffers.Builder, semanticsObjects: int):
    GeometryAddSemanticsObjects(builder, semanticsObjects)

def GeometryStartSemanticsObjectsVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartSemanticsObjectsVector(builder, numElems: int) -> int:
    return GeometryStartSemanticsObjectsVector(builder, numElems)

def GeometryEnd(builder: flatbuffers.Builder) -> int:
    return builder.EndObject()

def End(builder: flatbuffers.Builder) -> int:
    return GeometryEnd(builder)
