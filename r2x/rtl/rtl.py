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
""" Module Which Contains some base classes for the parsing and creation of RTL files"""

import os

from abc import *

from r2x.design import Design

class Parser(ABC):
    @staticmethod
    def strip_blank_lines(rtl:str) -> str:
        """Strips blank lines for the rtl.
        Blank lines here are any lines which contain exclusively white space.

        Args:
            rtl (str): The RTL string to strip blank lines from

        Returns:
            str: The RTL with blank lines stripped.
        """
        lines = rtl.splitlines()

        rtl = ""

        for line in lines :
            print(f'"{line}"')
            if line.strip() != '' :
                rtl += line + '\n'

        return rtl

    @abstractclassmethod
    def parse_rtl(cls, rtl:str) -> Design :
        pass

class Builder(ABC) :

    def __init__(self, tab_size:int=2, use_tab:bool=False, newline_chars:str="\n") :
        self.setup_newline(newline_chars)
        self.setup_tabs(tab_size, use_tab)

    @abstractmethod
    def write_rtl(self, design:Design, filename:str, fileheader:str=None) :
        pass

    @abstractmethod
    def design_to_string(self, design:Design) :
        pass

    @property
    def tab(self) :
        return " " * self._tab_size if not self._use_tab else "\t"

    @property
    def newline(self) :
        return self._newline_chars

    def setup_newline(self, newline_chars:str) :
        self._newline_chars = newline_chars

    def setup_tabs(self, tab_size:int=2, use_tab:bool=False) :
        self._tab_size = tab_size
        self._use_tab = use_tab

    def get_tab_size(self) :
        return self._tab_size

    def use_tab(self) :
        return self._use_tab