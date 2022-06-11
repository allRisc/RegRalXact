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
""" Module which contains all of the classes needed to represent an Memory-Mapped register bank """

from enum import Enum


class AccessType(Enum) :
    READ_WRITE = 0
    READ_ONLY = 1
    WRITE_ONLY = 2


def str2access(s:str) -> AccessType :
    s = s.lower().strip()

    if (s in ['read_only', 'ro']) :
        return AccessType.READ_ONLY
    elif (s in ['write_only', 'wo']) :
        return AccessType.WRITE_ONLY
    elif (s in ['read_write', 'rw']) :
        return AccessType.READ_WRITE
    else :
        raise ValueError(f"Invalid Access Type String '{s}'")


class BusInterface(Enum) :
    SRAM = 0
    AXI3 = 1
    AXI4 = 2


def str2bus(s:str) -> BusInterface :
    s = s.lower().strip()
    if (s == "sram") :
        return BusInterface.SRAM
    elif (s == 'axi3') :
        return BusInterface.AXI3
    elif (s == 'axi4') :
        return BusInterface.AXI4
    else :
        raise ValueError(f"Invalid Bus String '{s}'")


class Field :
    """ Class which represents a field of a register """

    def __init__(self, name, size:int=1,
                       access:AccessType=AccessType.READ_WRITE,
                       reset:str="0") :
        self.name = name
        self.size = size
        self.access = access
        self.reset = reset

    @property
    def name(self) -> str:
      return self._name

    @name.setter
    def name(self, name:str) :
        if (not isinstance(name, str)) :
            raise TypeError("Field Name Must be String")
        self._name = name

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size:int) :
        if (not isinstance(size, int)) :
            raise TypeError("Field size must be integer")
        self._size = size

    @property
    def access(self) -> AccessType :
        return self._access
    
    @access.setter
    def access(self, access:AccessType) :
        if (not isinstance(access, AccessType)) :
            raise TypeError("Field access must be a valid AccessType")
        self._access = access

    def __str__(self) -> str:
        return f"Field: {self.name} ({self.access}) - {self.size} [Reset: 0x{self.reset}]"

class Register :
    """ Class which represents a register """

    def __init__(self, name, access:AccessType=AccessType.READ_WRITE) :
        self.name = name
        self.access = access

        self._fields = []

    @property
    def name(self) -> str:
      return self._name

    @name.setter
    def name(self, name:str) :
        if (not isinstance(name, str)) :
            raise TypeError("Register Name Must be String")
        elif (" " in name) :
            raise ValueError("Register Names must not contain ' '")
        self._name = name

    @property
    def access(self) -> AccessType :
        return self._access
    
    @access.setter
    def access(self, access:AccessType) :
        if (not isinstance(access, AccessType)) :
            raise TypeError("Register access must be a valid AccessType")
        self._access = access

    def get_fields(self) -> list:
        return self._fields

    def add_field(self, f:Field) :
        if (not isinstance(f, Field)) :
            raise TypeError("Attempting to add non-field to register as a field")
        self._fields.append(f)

    def size(self) :
        s = 0
        for f in self._fields :
            s += f.size

        return s 

    def __str__(self) -> str:
        s = f"Register: {self.name} ({self.access})"
        for f in self._fields :
            s += "\n  " + str(f)
        return s


class Bank :
    """ Class which represents a register bank """
    
    def __init__(self, name:str, bus:BusInterface=BusInterface.SRAM, width:int=32) :
        self.name = name
        self.bus = bus
        self.width=width

        self._registers = []

    @property
    def name(self) -> str:
      return self._name

    @name.setter
    def name(self, name:str) :
        if (not isinstance(name, str)) :
            raise TypeError("Bank Name Must be String")
        self._name = name

    @property
    def width(self) -> int :
        return self._width

    @width.setter
    def width(self, width:int) :
        if (not isinstance(width, int)) :
            raise TypeError("Bank Name must be integer")
        self._width = width

    @property
    def bus(self) -> BusInterface :
        return self._bus
    
    @bus.setter
    def bus(self, bus:BusInterface) :
        if (not isinstance(bus, BusInterface)) :
            raise TypeError("Bank bus must be a valid BusInterface")
        self._bus = bus

    def get_registers(self) -> list:
        return self._registers

    def add_register(self, r:Register) :
        if (not isinstance(r, Register)) :
            raise TypeError("Attempting to add non-field to register as a field")
        self._registers.append(r)

    def __str__(self) -> str:
        s = f"Bank: {self.name} ({self.bus}, {self.width})"

        for r in self._registers :
            s += "\n" + str(r)

        s = s.replace("\n", "\n  ")

        return s