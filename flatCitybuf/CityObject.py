# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatCitybuf

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
from flatCitybuf.Column import Column
from flatCitybuf.GeographicalExtent import GeographicalExtent
from flatCitybuf.Geometry import Geometry
from typing import Optional
np = import_numpy()

class CityObject(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset: int = 0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = CityObject()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsCityObject(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # CityObject
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # CityObject
    def Type(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # CityObject
    def Id(self) -> Optional[str]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # CityObject
    def GeographicalExtent(self) -> Optional[GeographicalExtent]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            obj = GeographicalExtent()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # CityObject
    def Geometry(self, j: int) -> Optional[Geometry]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            obj = Geometry()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # CityObject
    def GeometryLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # CityObject
    def GeometryIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        return o == 0

    # CityObject
    def Attributes(self, j: int):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # CityObject
    def AttributesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # CityObject
    def AttributesLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # CityObject
    def AttributesIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        return o == 0

    # CityObject
    def Columns(self, j: int) -> Optional[Column]:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            obj = Column()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # CityObject
    def ColumnsLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # CityObject
    def ColumnsIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        return o == 0

    # CityObject
    def Children(self, j: int):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.String(a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return ""

    # CityObject
    def ChildrenLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # CityObject
    def ChildrenIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        return o == 0

    # CityObject
    def Parents(self, j: int):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.String(a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return ""

    # CityObject
    def ParentsLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # CityObject
    def ParentsIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        return o == 0

def CityObjectStart(builder: flatbuffers.Builder):
    builder.StartObject(8)

def Start(builder: flatbuffers.Builder):
    CityObjectStart(builder)

def CityObjectAddType(builder: flatbuffers.Builder, type: int):
    builder.PrependUint8Slot(0, type, 0)

def AddType(builder: flatbuffers.Builder, type: int):
    CityObjectAddType(builder, type)

def CityObjectAddId(builder: flatbuffers.Builder, id: int):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(id), 0)

def AddId(builder: flatbuffers.Builder, id: int):
    CityObjectAddId(builder, id)

def CityObjectAddGeographicalExtent(builder: flatbuffers.Builder, geographicalExtent: Any):
    builder.PrependStructSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(geographicalExtent), 0)

def AddGeographicalExtent(builder: flatbuffers.Builder, geographicalExtent: Any):
    CityObjectAddGeographicalExtent(builder, geographicalExtent)

def CityObjectAddGeometry(builder: flatbuffers.Builder, geometry: int):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(geometry), 0)

def AddGeometry(builder: flatbuffers.Builder, geometry: int):
    CityObjectAddGeometry(builder, geometry)

def CityObjectStartGeometryVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartGeometryVector(builder, numElems: int) -> int:
    return CityObjectStartGeometryVector(builder, numElems)

def CityObjectAddAttributes(builder: flatbuffers.Builder, attributes: int):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(attributes), 0)

def AddAttributes(builder: flatbuffers.Builder, attributes: int):
    CityObjectAddAttributes(builder, attributes)

def CityObjectStartAttributesVector(builder, numElems: int) -> int:
    return builder.StartVector(1, numElems, 1)

def StartAttributesVector(builder, numElems: int) -> int:
    return CityObjectStartAttributesVector(builder, numElems)

def CityObjectAddColumns(builder: flatbuffers.Builder, columns: int):
    builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(columns), 0)

def AddColumns(builder: flatbuffers.Builder, columns: int):
    CityObjectAddColumns(builder, columns)

def CityObjectStartColumnsVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartColumnsVector(builder, numElems: int) -> int:
    return CityObjectStartColumnsVector(builder, numElems)

def CityObjectAddChildren(builder: flatbuffers.Builder, children: int):
    builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(children), 0)

def AddChildren(builder: flatbuffers.Builder, children: int):
    CityObjectAddChildren(builder, children)

def CityObjectStartChildrenVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartChildrenVector(builder, numElems: int) -> int:
    return CityObjectStartChildrenVector(builder, numElems)

def CityObjectAddParents(builder: flatbuffers.Builder, parents: int):
    builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(parents), 0)

def AddParents(builder: flatbuffers.Builder, parents: int):
    CityObjectAddParents(builder, parents)

def CityObjectStartParentsVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartParentsVector(builder, numElems: int) -> int:
    return CityObjectStartParentsVector(builder, numElems)

def CityObjectEnd(builder: flatbuffers.Builder) -> int:
    return builder.EndObject()

def End(builder: flatbuffers.Builder) -> int:
    return CityObjectEnd(builder)
