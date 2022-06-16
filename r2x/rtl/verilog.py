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
""" Module Which Contains the System Verilog parsing and creation API """

from r2x.rtl.rtl import Parser, Builder
from r2x.util import *
from r2x.design import *

class VerilogParser(Parser) :
    pass

class VerilogBuilder(Builder) :
    pass

def strip_comments(rtl:str) -> str :
    """Strips comments out of an RTL string.
    The two types of system verilog comments are handled by this function.
    Block comments - ('/* [SOME COMMENT] */')
    Line comments - ('// [SOME COMMENT] \\n')

    Args:
        rtl (str): The RTL string to strip comments out of

    Returns:
        str: The RTL string with all comments striped out
    """
    # Handle block comments first
    while "/*" in rtl :
        open_pos = rtl.find("/*")
        close_pos = rtl.find("*/") + len("*/")

        rtl = rtl[:open_pos] + rtl[close_pos:]

    # Handle line comments next
    while "//" in rtl :
        pos = rtl.find("//")
        line_end = rtl.find("\n", pos)

        print(rtl[pos:line_end])
        rtl = rtl[:pos] + rtl[line_end:]

    return rtl