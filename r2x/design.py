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
from multiprocessing.sharedctypes import Value
import re
from abc import ABC

def _valid_id (s:str) -> bool :
  """Checks the input string is a valid ID for systemverilog or VHDL

  Args:
      s (str): The string to check

  Returns:
      bool: True if the input string is a valid ID, false otherwise
  """
  pattern = "^[A-Za-z0-9_]*$"
  return bool(re.match(pattern, s))

a
class AccessType (Enum) :
  READ_ONLY = 0
  WRITE_ONLY = 1
  READ_WRITE = 2

  @classmethod
  def str2access(cls, s:str) :
    """Converts the provided string to the specified AccessType.
    Valid access types for READ_ONLY are ['ro', 'read_only', 'read']
    Valid access types for WRITE_ONLY are ['wo', 'write_only', 'write']
    Valid access types for READ_WRITE are ['rw', 'read_write', 'readwrite']
    All strings are NOT case-sensitive

    Args:
        s (str): The string to convert to an AccessType

    Returns:
        AccessType: The corresponding AccessType
    """
    s = s.lower()
    if s == 'ro' or s == 'read_only' or s == 'read' :
      return cls.READ_ONLY
    if s == 'wo' or s == 'write_only' or s == 'write' :
      return cls.READ_ONLY
    if s == 'rw' or s == 'read_write' or s == 'readwrite' :
      return cls.READ_ONLY
    raise ValueError(f"Invalid Access Type string ({s})")


class PortDirection (Enum) :
  INPUT = 0
  OUTPUT = 1
  INOUT = 1

  @classmethod
  def str2direction(cls, s:str) :
    """Converts the provided string to the specified Direction.
    Valid access types for INPUT are ['in', 'input']
    Valid access types for OUTPUT are ['out', 'output']
    Valid access types for INOUT are ['inout', 'input_output']
    All strings are NOT case-sensitive

    Args:
        s (str): The string to convert to an AccessType

    Returns:
        AccessType: The corresponding AccessType
    """
    s = s.lower()
    if s == 'in' or s == 'input' :
      return cls.INPUT
    if s == 'out' or s == 'output' :
      return cls.OUTPUT
    if s == 'inout' or s == 'input_output' :
      return cls.INOUT
    raise ValueError(f"Invalid Access Type string ({s})")


class Component :
  @property
  def name(self) -> str :
    """The Component Name

    Returns:
        str: The component name
    """
    return self._name

  @name.setter
  def name(self, n:str) :
    """Assign the component's name

    Args:
        n (str): The name of the component
    """
    if not _valid_id :
      raise ValueError(f"{type(self).__name__} name: {n} is invalid. Must only contain '_' and alpha-numeric characters")
    self._name = n


class MemoryComponent (Component) :
  @property
  def access(self) -> AccessType :
    """The MemoryComponent's access-type

    Returns:
        AccessType: The access type of the component
    """
    return self._access

  @access.setter
  def access(self, acc) :
    if (isinstance(acc, str)) :
      self._access = AccessType.str2access(acc)
    elif isinstance(acc, AccessType) :
      self._access = acc
    else :
      raise TypeError(f"{type(self).__name__} access must be either string or AccessType")


class Signal (Component) :
  def __init__ (self, name:str, width:int=1) :
    self.name = name
    self.width = width

  @property
  def width(self) -> int :
    """The signal width

    Returns:
        int: The width of the signal
    """
    return self._width

  @width.setter
  def width(self, w:int) :
    if w <= 0 :
      raise ValueError(f"{type(self).__name__} width cannot be less than 1!")
    elif not isinstance(w, int) :
      raise TypeError(f"{type(self).__name__} width must be an integer!")
    else :
      self._width = w


class Field (MemoryComponent, Signal) :
  
  def __init__ (self, name:str, access, width:int=1) :
    self.name = name
    self.access = access
    self.width = width


class Register (MemoryComponent, Signal) :
  
  def __init__ (self, name:str, access, width:int=1) :
    self.name = name
    self.access = access
    self.width = width


class Port (signal) :
  def __init__ (self, name:str, dir:PortDirection, width:int=1) :
    self.name = name
    self.direction = dir
    self.width = width

  @property
  def direction(self) -> AccessType :
    """The MemoryComponent's access-type

    Returns:
        AccessType: The access type of the component
    """
    return self._access

  @direction.setter
  def direction(self, dir) :
    if (isinstance(dir, str)) :
      self._access = PortDirection.str2direction(dir)
    elif isinstance(dir, PortDirection) :
      self._access = dir
    else :
      raise TypeError(f"{type(self).__name__} direction must be either string or PortDirection")

class Parameter :
  pass

class Module :
  pass
