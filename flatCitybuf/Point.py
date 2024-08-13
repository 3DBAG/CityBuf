# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatCitybuf

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
np = import_numpy()

class Point(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls) -> int:
        return 8

    # Point
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Point
    def Vertex(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Point
    def SemanticObjectId(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))

def CreatePoint(builder, vertex, semanticObjectId):
    builder.Prep(4, 8)
    builder.PrependUint32(semanticObjectId)
    builder.PrependUint32(vertex)
    return builder.Offset()
