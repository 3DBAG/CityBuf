# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CityBuf_

import flatbuffers
from flatbuffers.compat import import_numpy
from typing import Any
np = import_numpy()

class SemanticObject(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset: int = 0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = SemanticObject()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsSemanticObject(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # SemanticObject
    def Init(self, buf: bytes, pos: int):
        self._tab = flatbuffers.table.Table(buf, pos)

    # SemanticObject
    def Type(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # SemanticObject
    def Attributes(self, j: int):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # SemanticObject
    def AttributesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # SemanticObject
    def AttributesLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # SemanticObject
    def AttributesIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # SemanticObject
    def Children(self, j: int):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # SemanticObject
    def ChildrenAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint32Flags, o)
        return 0

    # SemanticObject
    def ChildrenLength(self) -> int:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # SemanticObject
    def ChildrenIsNone(self) -> bool:
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

    # SemanticObject
    def Parent(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

def SemanticObjectStart(builder: flatbuffers.Builder):
    builder.StartObject(4)

def Start(builder: flatbuffers.Builder):
    SemanticObjectStart(builder)

def SemanticObjectAddType(builder: flatbuffers.Builder, type: int):
    builder.PrependUint8Slot(0, type, 0)

def AddType(builder: flatbuffers.Builder, type: int):
    SemanticObjectAddType(builder, type)

def SemanticObjectAddAttributes(builder: flatbuffers.Builder, attributes: int):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(attributes), 0)

def AddAttributes(builder: flatbuffers.Builder, attributes: int):
    SemanticObjectAddAttributes(builder, attributes)

def SemanticObjectStartAttributesVector(builder, numElems: int) -> int:
    return builder.StartVector(1, numElems, 1)

def StartAttributesVector(builder, numElems: int) -> int:
    return SemanticObjectStartAttributesVector(builder, numElems)

def SemanticObjectAddChildren(builder: flatbuffers.Builder, children: int):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(children), 0)

def AddChildren(builder: flatbuffers.Builder, children: int):
    SemanticObjectAddChildren(builder, children)

def SemanticObjectStartChildrenVector(builder, numElems: int) -> int:
    return builder.StartVector(4, numElems, 4)

def StartChildrenVector(builder, numElems: int) -> int:
    return SemanticObjectStartChildrenVector(builder, numElems)

def SemanticObjectAddParent(builder: flatbuffers.Builder, parent: int):
    builder.PrependUint32Slot(3, parent, 0)

def AddParent(builder: flatbuffers.Builder, parent: int):
    SemanticObjectAddParent(builder, parent)

def SemanticObjectEnd(builder: flatbuffers.Builder) -> int:
    return builder.EndObject()

def End(builder: flatbuffers.Builder) -> int:
    return SemanticObjectEnd(builder)
