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

from ast import Param
from r2x.rtl.rtl import Parser, Builder
from r2x.design import *

from datetime import date

class VerilogParser(Parser) :
    def parse_rtl(cls, rtl:str) -> Design :
        pass

class VerilogBuilder(Builder) :
    
    def __init__(self, tab_size:int=2, use_tab:bool=False, newline_chars:str="\n") :
        super().__init__(tab_size, use_tab, newline_chars)

    def write_rtl(self, design:Design, filename:str, fileheader:str=None) :
        if fileheader is None :
            fileheader = f"// RegRalXACT Output RTL {date.today().strftime('%b %d, %Y')}"

        rtl = fileheader + "\n\n" + self.design_to_string(design)

        with open(filename, 'w') as f :
            f.write(rtl)

    @classmethod
    def create_parameter(cls, param:Param) -> str:
        """Create the line for the parameter definition in verilog

        Args:
            param (Param): The parameter to create the parameter definition for

        Returns:
            str: The parameter definition without leading tab or trailing comma/newline
        """
        retval = f"parameter "

        if (param.ptype == ParamType.NONE) :
            pass
        elif (param.ptype == ParamType.INTEGER) :
            retval += "int "
        elif (param.ptype == ParamType.FLOAT) :
            retval += "real "
        elif (param.ptype == ParamType.BOOL) :
            retval += "bool "
        elif (param.ptype == ParamType.BIT_VALUES) :
            pass
        elif (param.ptype == ParamType.STRING) :
            retval += "string "

        retval = f"{param.name}"

        if not param.default is None :
            retval += f" = {param.default}"

        return retval

    @classmethod
    def create_port(cls, port:Port) :
        """Creates the line for the port definition in verilog

        Args:
            port (Port): The port to create the port definition for

        Returns:
            str: The port definition without leading tab or trailing comma/newline
        """
        retval = ""

        if (port.direction == PortDirection.INOUT) :
            retval += "inout  "
        elif (port.direction == PortDirection.OUTPUT) :
            retval += "output "
        elif (port.direction == PortDirection.INPUT) :
            retval += "input  "

        if (port.ptype == PortType.REG) :
            retval += "reg   "
        elif (port.ptype == PortType.WIRE) :
            retval += "wire  "
        elif (port.ptype == PortType.LOGIC) :
            retval += "logic "

        if isinstance(port.size, list) :
            raise NotImplementedError("Multi-dimensional ports are not currently supported by RegRalXACT")
        elif port.size > 1 :
            retval += f"[{port.size -1}:0] " 
        else :
            retval += " " * 5
        
        retval += port.name

        return retval

    def design_to_string(self, design:Design) -> str:
        """Creates the Verilog RTL string from the provided design

        Args:
            design (Design): The design to create the RTL based on

        Returns:
            str: The RTL in verilog based on the provided design
        """
        
        rtl = ""
        
        # Module definition
        rtl += f"module {design.name}"

        if design.has_params() :
            rtl += f" #({self.newline}"

            for p in design.get_params() :
                if p != design.get_params()[-1] :
                    rtl += f"{self.tab}{self.create_parameter(p)},{self.newline}"
                else :
                    rtl += f"{self.tab}{self.create_parameter(p)}{self.newline}"

            rtl += ")"

        if design.has_ports() :
            rtl += f" ({self.newline}"

            for p in design.get_ports() :
                if p != design.get_ports()[-1] :
                    rtl += f"{self.tab}{self.create_port(p)},{self.newline}"
                else :
                    rtl += f"{self.tab}{self.create_port(p)}{self.newline}"

            rtl += ")"
        else :
            rtl += "( )"

        rtl += f";{self.newline * 2}"

        sig_defs = ""
        sub_defs = ""

        # Handle bank creation
        if design.has_banks() :
            raise NotImplementedError ("VerilogBuilder does not currently support designs with banks")

        # Handle submodule stitching
        if design.has_submodules() :
            raise NotImplementedError ("VerilogBuilder does not currently support designs with submodules")

        rtl += f"endmodule{self.newline}"

        return rtl
