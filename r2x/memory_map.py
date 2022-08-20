############################################################################
# A python API which supports the automatic creation of memory mapped
#   register interfaces
# Copyright (C) 2022 allRisc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

from enum import Enum
from abc import ABC, abstractmethod

class AccessType(Enum) :
  """All of the permissable access types for a Field or Register in a MemoryMap/Address Bank
  """

  RO = "RO"
  """Read Only"""

  RW = "RW"
  """Read-Write"""

  WO = "WO"
  """Write Only"""

  ReturnToZero = "RTZ"
  """Return to Zero"""

  @classmethod
  def from_str(cls, s:str) :
    """Converts the string to a specified access type

    Args:
        s (str): The string to convert

    Raises:
      ValueError: If the string cannot be properly converted

    Returns:
        AccessType: The corresponding access type
    """
    s = s.replace(" ","").lower()

    if s in ['ro', 'read-only', 'readonly'] :
      return AccessType.RO
    if s in ['rw', 'read-write', 'readwrite'] :
      return AccessType.RW
    if s in ['wo', 'write-only', 'writeonly'] :
      return AccessType.WO
    if s in ['rtz', 'returntozero', 'return-to-zero'] :
      return AccessType.RO
    raise ValueError(f"{s} is not a valid string for an AccessType")


class MemoryComponent (ABC) :
  """Abstract Class which contains the common aspects of a MemoryComponent (Field, Register, AddressBank)
  """
  def __init__(self, name:str="", accessType:AccessType=AccessType.RW,
                     offset:int=0, volatile:bool=False, reserved:bool=False) :
    """Create a Memory Component

    Args:
        name (str, optional): The name of the memory component. Defaults to "".
        accessType (AccessType, optional): The access type for the memory element. Defaults to AccessType.RW.
        offset (int, optional): The relative offset for the memory element. Defaults to 0.
        volatile (bool, optional): Whether the memory component is volatile. Defaults to False.
        reserved (bool, optional): Whether the memory component is reserved. Defaults to False.
    """
    self.name = name
    self.accessType = accessType
    self.offset = offset
    self.volatile = volatile
    self.reserved = reserved

  @property
  def name(self) -> str :
    """The memory component name"""
    return self._name

  @name.setter
  def name(self, name:str) :
    if not isinstance(name, str) :
      raise TypeError(f"MemoryComponent name must be valid string (not '{name}')")
    self._name = name

  @property
  def accessType(self) -> str :
    """The memory component accessType"""
    return self._accessType

  @accessType.setter
  def accessType(self, accessType:AccessType) :
    if not isinstance(accessType, AccessType) :
      raise TypeError(f"MemoryComponent accessType must be valid AccessType (not '{accessType}')")
    self._accessType = accessType

  @property
  def offset(self) -> int :
    """The memory component offset"""
    return self._offset

  @offset.setter
  def offset(self, offset:int) :
    if isinstance(offset, (int, float)) :
      self._offset = int(offset)
    
    try:
      self._offset = int(offset)
    except :
      raise TypeError(f"MemoryComponent offset must be int or convertible to int through the 'int()' method (not '{offset}')")

  @property
  def volatile(self) -> bool:
    """Whether the MemoryComponent is volatile"""
    return self._volatile

  @volatile.setter
  def volatile(self, volatile:bool) :
    if not isinstance(volatile, bool) :
      raise TypeError(f"MemoryComponent volatile must be a boolean value")
    self._volatile = volatile

  @property
  def reserved(self) -> bool:
    """Whether the MemoryComponent is reserved"""
    return self._reserved

  @reserved.setter
  def reserved(self, reserved:bool) :
    if not isinstance(reserved, bool) :
      raise TypeError(f"MemoryComponent reserved must be a boolean value")
    self._reserved = reserved

  @classmethod
  @abstractmethod
  def from_dict(cls, d:dict) : pass

  @abstractmethod
  def to_dict(self) -> dict : pass


class Field (MemoryComponent):
  """Class which represents a register field
  """
  def __init__(self, name:str="", accessType:AccessType=AccessType.RW,
                     offset:int=0, volatile:bool=False, reserved:bool=False,
                     width:int=0, reset:int=0) :
    """Create a Field

    Args:
        name (str, optional): The name of the field. Defaults to "".
        accessType (AccessType, optional): The access type for the field. Defaults to AccessType.RW.
        offset (int, optional): The relative offset for the field. Defaults to 0.
        volatile (bool, optional): Whether the field is volatile. Defaults to False.
        reserved (bool, optional): Whether the field is reserved. Defaults to False.
        width (int, optional): The bit-width of the field. Defaults to 0.
        reset (int, optional): The reset value of the field. Defaults to 0.
    """
    super().__init__(name, accessType, offset, volatile, reserved)
    self.width = width
    self.reset = reset

  @property
  def width(self) -> int:
    """The width of the field in bits"""
    return self._width

  @width.setter
  def width(self, width:int) :
    if isinstance(width, (int, float)) :
      self._width = int(width)
    
    try:
      self._width = int(width)
    except :
      raise TypeError(f"Field width must be int or convertible to int through the 'int()' method (not '{width}')")

  @property
  def reset(self) -> int:
    """The reset of the field in bits"""
    return self._reset

  @reset.setter
  def reset(self, reset:int) :
    if isinstance(reset, (int, float)) :
      self._reset = int(reset)
    
    try:
      self._reset = int(reset)
    except :
      raise TypeError(f"Field reset must be int or convertible to int through the 'int()' method (not '{reset}')")

  @classmethod
  def from_dict(cls, d:dict):
    """Converts the dictionary representation of the field to a Field object
    
    Args:
        d (dict): The dictionary to build the field from.
      
    Returns:
        Field: The field object derived from the dictionary
    """
    for req in ['name', 'accessType', 'offset', 'width', 'reset'] :
      if not req in d :
        raise ValueError(f"Field dictionary missing required key: {req}")

    fld = Field(name=d['name'], accessType=d['accessType'], offset=d['offset'], width=d['width'], reset=d['reset'])

    if 'volatile' in d :
      fld.volatile = d['volatile']

    if 'reserved' in d :
      fld.reserved = d['reserved']

    return fld

  def to_dict(self) -> dict :
    """Creates a dictionary representation of the field

    Returns:
        dict: The dictionary representation of the field
    """
    return {
      "name" : self.name,
      "accessType": self.accessType.value,
      "offset": self.offset,
      "width": self.width,
      "reset": self.reset,
      "volatile": self.volatile,
      "reserved": self.reserved
    }

class Register (MemoryComponent):
  """Class which represents a register
  """

  def __init__(self, name:str="", accessType:AccessType=AccessType.RW,
                     offset:int=0, volatile:bool=False, reserved:bool=False,
                     dimension:int=1):
    super().__init__(name, accessType, offset, volatile, reserved)
    self.dimension = dimension
    self._current_size = 0
    self.fields = []

  @property
  def dimension(self) -> int:
    """The dimension of the register"""
    return self._dimension

  @dimension.setter
  def dimension(self, dimension:int) :
    if isinstance(dimension, (int, float)) :
      self._dimension = int(dimension)
    
    try:
      self._dimension = int(dimension)
    except :
      raise TypeError(f"Register dimension must be int or convertible to int through the 'int()' method (not '{dimension}')")

  def add_field(self, fld:Field) :
    """Adds a field to the given register

    Args:
        fld (Field): The field to add to the register
    """
    self.fields.append(fld)
    self._current_size += fld.width

  @classmethod
  def from_dict(cls, d:dict):
    """Converts the dictionary representation of the register to a Register object
    
    Args:
        d (dict): The dictionary to build the register from.
      
    Returns:
        Register: The register object derived from the dictionary
    """
    for req in ['name', 'accessType', 'offset'] :
      if not req in d :
        raise ValueError(f"Register dictionary missing required key: {req}")

    reg = Register(name=d['name'], accessType=d['accessType'], offset=d['offset'])

    if 'volatile' in d :
      reg.volatile = d['volatile']

    if 'reserved' in d :
      reg.reserved = d['reserved']

    if 'dimension' in d :
      reg.dimension = d['dimension']

    for fld in d['fields'] :
      if not 'offset' in fld :
        fld['offset'] = reg._current_size
      reg.add_field(Field.from_dict(fld))

    return reg

  def to_dict(self) -> dict :
    """Creates a dictionary representation of the register

    Returns:
        dict: The dictionary representation of the register
    """
    return {
      "name" : self.name,
      "accessType": self.accessType.value,
      "offset": self.offset,
      "dimension": self.dimension,
      "volatile": self.volatile,
      "reserved": self.reserved,
      "fields": [f.to_dict() for f in self.fields]
    }

class AddressBank (MemoryComponent):
  """Class which represents an Address Bank
  """

  def __init__(self, name:str="", accessType:AccessType=AccessType.RW,
                     offset:int=0, volatile:bool=False, reserved:bool=False,
                     regSize:int=32):
    super().__init__(name, accessType, offset, volatile, reserved)
    self.regSize = regSize
    
    self.registers = []
    self._current_size = 0

  def add_register(self, reg:Register) :
    """Adds a register to the address bank

    Args:
        reg (Register): The register to add to the address bank
    """
    if reg.offset >= self._current_size :
      self._current_size = reg.offset  
    self._current_size += round(reg.dimension * self.regSize / 8)
    self.registers.append(reg)

  @classmethod
  def from_dict(cls, d:dict):
    """Converts the dictionary representation of the Address Bank to a AddressBank object
    
    Args:
        d (dict): The dictionary to build the AddressBank from.
      
    Returns:
        AddressBank: The AddressBank object derived from the dictionary
    """
    for req in ['name', 'accessType', 'offset', 'regSize'] :
      if not req in d :
        raise ValueError(f"AddressBank dictionary missing required key: {req}")

    addr_bank = AddressBank(name=d['name'], accessType=d['accessType'], offset=d['offset'], regSize=d['regSize'])

    if 'volatile' in d :
      addr_bank.volatile = d['volatile']

    if 'reserved' in d :
      addr_bank.reserved = d['reserved']

    for reg in d['registers'] :
      if not 'offset' in reg :
        reg['offset'] = reg._current_size
      addr_bank.add_register(Register.from_dict(reg))

    return addr_bank

  def to_dict(self) -> dict :
    """Creates a dictionary representation of the register

    Returns:
        dict: The dictionary representation of the register
    """
    return {
      "name" : self.name,
      "accessType": self.accessType.value,
      "offset": self.offset,
      "regSize": self.regSize,
      "volatile": self.volatile,
      "reserved": self.reserved,
      "registers": [r.to_dict() for r in self.registers]
    }

class MemoryMap:
  """Class which represents a MemoryMap.
  Contains a set of AddressBanks
  """

  def __init__(self, name:str) :
    self.name = name
    self.banks = []

  def add_bank(self, bank:AddressBank) :
    """Adds the AddressBank to the MemoryMap

    Args:
        bank (AddressBank): The address bank to add
    """
    self.banks.append(bank)

  @property
  def name(self) -> str :
    """The memory map name"""
    return self._name

  @name.setter
  def name(self, name:str) :
    if not isinstance(name, str) :
      raise TypeError(f"MemoryMap name must be valid string (not '{name}')")
    self._name = name

  @classmethod
  def from_dict(cls, d:dict) :
    """Converts the dictionary representation of the Memory Map to a MemoryMap object
    
    Args:
        d (dict): The dictionary to build the MemoryMap from.
      
    Returns:
        MemoryMap: The MemoryMap object derived from the dictionary
    """
    for req in ['name'] :
      if not req in d :
        raise ValueError(f"MemoryMap dictionary missing required key: {req}")

    mmap = MemoryMap(name=d['name'])

    for bank in d['banks'] :
      mmap.add_bank(AddressBank.from_dict(bank))

    return mmap

  def to_dict(self) -> dict :
    """Creates a dictionary representation of the register

    Returns:
        dict: The dictionary representation of the register
    """
    return {
      "name" : self.name,
      "banks": [b.to_dict() for b in self.banks]
    }