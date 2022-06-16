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

from r2x.util import *
from r2x.design import *

import r2x.rtl.verilog as verilog

def to_design(rtl:str) -> Design :
    rtl = verilog.strip_comments(rtl)
    print(f'"{rtl}"')
    rtl = verilog.strip_blank_lines(rtl)
    print(f'"{rtl}"')
    
    raise NotImplementedError("r2x.rtl.verilog.verilog_to_design not currently implemented")
