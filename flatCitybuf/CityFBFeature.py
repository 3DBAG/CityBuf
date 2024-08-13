# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatCitybuf

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
from flatCitybuf.CityObject import CityObject
from flatCitybuf.Vertex import Vertex
from typing import Optional
np = import_numpy()

class CityFBFeature(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset: int = 0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = CityFBFeature()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsCityFBFeature(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # CityFBFeature
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # CityFBFeature
    def Id(self) -> Optional[str]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # CityFBFeature
    def Objects(self, j: int) -> Optional[CityObject]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            obj = CityObject()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # CityFBFeature
    def ObjectsLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # CityFBFeature
    def ObjectsIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # CityFBFeature
    def Vertices(self, j: int) -> Optional[Vertex]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 12
            obj = Vertex()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # CityFBFeature
    def VerticesLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # CityFBFeature
    def VerticesIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

def CityFBFeatureStart(builder: flatbuffers.Builder):
    builder.StartObject(3)

def Start(builder: flatbuffers.Builder):
    CityFBFeatureStart(builder)

def CityFBFeatureAddId(builder: flatbuffers.Builder, id: int):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(id), 0)

def AddId(builder: flatbuffers.Builder, id: int):
    CityFBFeatureAddId(builder, id)

def CityFBFeatureAddObjects(builder: flatbuffers.Builder, objects: int):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(objects), 0)

def AddObjects(builder: flatbuffers.Builder, objects: int):
    CityFBFeatureAddObjects(builder, objects)

def CityFBFeatureStartObjectsVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartObjectsVector(builder, numElems: int) -> int:
    return CityFBFeatureStartObjectsVector(builder, numElems)

def CityFBFeatureAddVertices(builder: flatbuffers.Builder, vertices: int):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(vertices), 0)

def AddVertices(builder: flatbuffers.Builder, vertices: int):
    CityFBFeatureAddVertices(builder, vertices)

def CityFBFeatureStartVerticesVector(builder, numElems: int) -> int:
    return builder.StartVector(12, numElems, 4)

def StartVerticesVector(builder, numElems: int) -> int:
    return CityFBFeatureStartVerticesVector(builder, numElems)

def CityFBFeatureEnd(builder: flatbuffers.Builder) -> int:
    return builder.EndObject()

def End(builder: flatbuffers.Builder) -> int:
    return CityFBFeatureEnd(builder)
