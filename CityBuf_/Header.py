# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CityBuf_

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
from CityBuf_.Column import Column
from CityBuf_.Crs import Crs
from CityBuf_.GeographicalExtent import GeographicalExtent
from CityBuf_.Transform import Transform
from typing import Optional
np = import_numpy()

class Header(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset: int = 0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Header()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsHeader(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Header
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Header
    def GeographicalExtent(self) -> Optional[GeographicalExtent]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = o + self._tab.Pos
            obj = GeographicalExtent()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Header
    def Transform(self) -> Optional[Transform]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = o + self._tab.Pos
            obj = Transform()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Header
    def Columns(self, j: int) -> Optional[Column]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            obj = Column()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Header
    def ColumnsLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Header
    def ColumnsIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

    # Header
    def FeaturesCount(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint64Flags, o + self._tab.Pos)
        return 0

    # Header
    def Crs(self) -> Optional[Crs]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            obj = Crs()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Header
    def Metadata(self) -> Optional[str]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def HeaderStart(builder: flatbuffers.Builder):
    builder.StartObject(6)

def Start(builder: flatbuffers.Builder):
    HeaderStart(builder)

def HeaderAddGeographicalExtent(builder: flatbuffers.Builder, geographicalExtent: Any):
    builder.PrependStructSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(geographicalExtent), 0)

def AddGeographicalExtent(builder: flatbuffers.Builder, geographicalExtent: Any):
    HeaderAddGeographicalExtent(builder, geographicalExtent)

def HeaderAddTransform(builder: flatbuffers.Builder, transform: Any):
    builder.PrependStructSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(transform), 0)

def AddTransform(builder: flatbuffers.Builder, transform: Any):
    HeaderAddTransform(builder, transform)

def HeaderAddColumns(builder: flatbuffers.Builder, columns: int):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(columns), 0)

def AddColumns(builder: flatbuffers.Builder, columns: int):
    HeaderAddColumns(builder, columns)

def HeaderStartColumnsVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartColumnsVector(builder, numElems: int) -> int:
    return HeaderStartColumnsVector(builder, numElems)

def HeaderAddFeaturesCount(builder: flatbuffers.Builder, featuresCount: int):
    builder.PrependUint64Slot(3, featuresCount, 0)

def AddFeaturesCount(builder: flatbuffers.Builder, featuresCount: int):
    HeaderAddFeaturesCount(builder, featuresCount)

def HeaderAddCrs(builder: flatbuffers.Builder, crs: int):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(crs), 0)

def AddCrs(builder: flatbuffers.Builder, crs: int):
    HeaderAddCrs(builder, crs)

def HeaderAddMetadata(builder: flatbuffers.Builder, metadata: int):
    builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(metadata), 0)

def AddMetadata(builder: flatbuffers.Builder, metadata: int):
    HeaderAddMetadata(builder, metadata)

def HeaderEnd(builder: flatbuffers.Builder) -> int:
    return builder.EndObject()

def End(builder: flatbuffers.Builder) -> int:
    return HeaderEnd(builder)