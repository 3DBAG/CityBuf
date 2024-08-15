# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CityBuf_

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
from typing import Optional
np = import_numpy()

class Crs(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset: int = 0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Crs()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsCrs(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Crs
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Crs
    def Authority(self) -> Optional[str]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Crs
    def Version(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Crs
    def Code(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def CrsStart(builder: flatbuffers.Builder):
    builder.StartObject(3)

def Start(builder: flatbuffers.Builder):
    CrsStart(builder)

def CrsAddAuthority(builder: flatbuffers.Builder, authority: int):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(authority), 0)

def AddAuthority(builder: flatbuffers.Builder, authority: int):
    CrsAddAuthority(builder, authority)

def CrsAddVersion(builder: flatbuffers.Builder, version: int):
    builder.PrependInt32Slot(1, version, 0)

def AddVersion(builder: flatbuffers.Builder, version: int):
    CrsAddVersion(builder, version)

def CrsAddCode(builder: flatbuffers.Builder, code: int):
    builder.PrependInt32Slot(2, code, 0)

def AddCode(builder: flatbuffers.Builder, code: int):
    CrsAddCode(builder, code)

def CrsEnd(builder: flatbuffers.Builder) -> int:
    return builder.EndObject()

def End(builder: flatbuffers.Builder) -> int:
    return CrsEnd(builder)