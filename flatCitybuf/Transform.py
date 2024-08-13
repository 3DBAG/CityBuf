# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatCitybuf

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
np = import_numpy()

class Transform(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls) -> int:
        return 48

    # Transform
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Transform
    def Scale(self, obj):
        obj.Init(self._tab.Bytes, self._tab.Pos + 0)
        return obj

    # Transform
    def Translate(self, obj):
        obj.Init(self._tab.Bytes, self._tab.Pos + 24)
        return obj


def CreateTransform(builder, scale_x, scale_y, scale_z, translate_x, translate_y, translate_z):
    builder.Prep(8, 48)
    builder.Prep(8, 24)
    builder.PrependFloat64(translate_z)
    builder.PrependFloat64(translate_y)
    builder.PrependFloat64(translate_x)
    builder.Prep(8, 24)
    builder.PrependFloat64(scale_z)
    builder.PrependFloat64(scale_y)
    builder.PrependFloat64(scale_x)
    return builder.Offset()
