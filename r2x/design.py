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
""" Module which contains all of the classes needed to represent an RTL design """

from enum import Enum
from r2x.bank import *


class PortType(Enum) :
    WIRE = 0
    REG = 1
    LOGIC = 2


class PortDirection(Enum) :
    INPUT = 0
    OUTPUT = 1
    INOUT = 2


class Port :
    """ Class which represents an RTL Port """

    def __init__(self, name:str, direction:PortDirection=PortDirection.INOUT,
                       size:int=1,
                       ptype:PortType=PortType.WIRE ):
        self.name = name
        self.direction = direction
        self.size = size
        self.ptype = ptype

    @property
    def name(self) -> str:
      return self._name

    @name.setter
    def name(self, name:str) :
        if (not isinstance(name, str)) :
            raise TypeError("Port Name Must be String")
        self._name = name

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size) :
        if (isinstance(size, list)) :
            for s in size :
                if (not isinstance(s, int)) :
                    raise TypeError("Port size lists must contain only integers")
        elif (not isinstance(size, int)) :
            raise TypeError("Port size must be integer or list of integers")
        self._size = size

    @property
    def ptype(self) -> PortType:
        return self._ptype

    @ptype.setter
    def ptype(self, ptype:PortType) :
        if (not isinstance(ptype, PortType)) :
            raise TypeError("Port ptype must be a valid PortType")
        self._ptype = ptype

    @property
    def direction(self) -> PortDirection :
        return self._direction
    
    @direction.setter
    def direction(self, direction:PortDirection) :
        if (not isinstance(direction, PortDirection)) :
            raise TypeError("Port direction must be a valid PortDirection")
        self._direction = direction


class ParamType (Enum) :
    NONE = 0
    INTEGER = 1
    FLOAT = 2
    BOOL = 3
    BIT_VALUES = 4
    STRING = 5

class Param :
    """ Class which represents an RTL parameter"""
    
    def __init__(self, name, ptype:ParamType=ParamType.NONE,
                       default=None):
        self.name = name
        self.ptype = ptype
        self.default = default

    @property
    def name(self) -> str:
      return self._name

    @name.setter
    def name(self, name:str) :
        if (not isinstance(name, str)) :
            raise TypeError("Parameter Name Must be String")
        self._name = name

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, default) :
        self._default = default

    @property
    def ptype(self) -> ParamType:
        return self._ptype

    @ptype.setter
    def ptype(self, ptype:ParamType) :
        if (not isinstance(ptype, ParamType)) :
            raise TypeError("Param ptype must be a valid ParamType")
        self._ptype = ptype

class Design :
    """ Class which represents an RTL design """

    def __init__(self, name:str) :
        self.name = name

        self._ports = []
        self._parameters = []
        self._banks = {}
        self._submodules = {}

    @property
    def name(self) -> str:
      return self._name

    @name.setter
    def name(self, name:str) :
        if (not isinstance(name, str)) :
            raise TypeError("Bank Name Must be String")
        self._name = name

    def has_params(self) -> bool :
        return len(self._parameters) != 0

    def get_params(self) -> list :
        return self._parameters

    def has_ports(self) -> bool :
        return len(self._ports) != 0

    def get_ports(self) -> list :
        return self._ports

    def has_banks(self) -> bool :
        return len(self._banks) != 0

    def has_submodules(self) -> bool :
        return len(self._submodules) != 0

