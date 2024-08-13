# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatCitybuf

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
np = import_numpy()

class LineString(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset: int = 0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = LineString()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsLineString(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # LineString
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # LineString
    def Points(self, j: int):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # LineString
    def PointsAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint32Flags, o)
        return 0

    # LineString
    def PointsLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # LineString
    def PointsIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # LineString
    def SemanticObjectId(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

def LineStringStart(builder: flatbuffers.Builder):
    builder.StartObject(2)

def Start(builder: flatbuffers.Builder):
    LineStringStart(builder)

def LineStringAddPoints(builder: flatbuffers.Builder, points: int):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(points), 0)

def AddPoints(builder: flatbuffers.Builder, points: int):
    LineStringAddPoints(builder, points)

def LineStringStartPointsVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartPointsVector(builder, numElems: int) -> int:
    return LineStringStartPointsVector(builder, numElems)

def LineStringAddSemanticObjectId(builder: flatbuffers.Builder, semanticObjectId: int):
    builder.PrependUint32Slot(1, semanticObjectId, 0)

def AddSemanticObjectId(builder: flatbuffers.Builder, semanticObjectId: int):
    LineStringAddSemanticObjectId(builder, semanticObjectId)

def LineStringEnd(builder: flatbuffers.Builder) -> int:
    return builder.EndObject()

def End(builder: flatbuffers.Builder) -> int:
    return LineStringEnd(builder)
