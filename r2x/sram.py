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

from io import TextIOWrapper
from mimetypes import common_types

import r2x.reg_bank as reg_bank
from r2x import RTL
from r2x.system_verilog import *

def create_sram(filename:str, mem_map:dict, header:str="", lang:RTL=RTL.SystemVerilog) :
  with open(filename, "w") as f:
    f.write(header)

    _write_sram_module_definition(f, mem_map)

    _write_sram_local_params(f, mem_map)

def _write_sram_module_definition(file:TextIOWrapper, mem_map:dict) :
  """Writes the module definition for the SRAM

  Args:
      file (TextIOWrapper): The writable file to output the SRAM bank to
      mem_map (dict): The memory map definition for the SRAM bank
  """
  file.write(f"module {mem_map['name']}_sram #(\n")
  
  file.write(parameter("ADDR_WIDTH", default=32, ptype="int", tabs=1))
  file.write(parameter("DATA_WIDTH", default=32, ptype="int", tabs=1))
  file.write(parameter("STRB_WIDTH", default=32, ptype="int", tabs=1))

  file.write(") (\n")

  file.write(port("clk", "input", tabs=1))
  file.write(port("rst_low", "input", tabs=1))
  file.write("\n")

  reg_bank._write_reg_ports(file, mem_map)
  file.write("\n")

  file.write(comment_block("SRAM-Like Signals", tabs=1, mod=True))
  file.write(comment("Write Channel"))
  file.write(port("wr_addr", "input", width="ADDR_WIDTH", tabs=1))
  file.write(port("wr_data", "input", width="DATA_WIDTH", tabs=1))
  file.write(port("wr_strb", "input", width="STRB_WIDTH", tabs=1))
  file.write(port("wr_en",   "input", width=1, tabs=1))
  file.write(comment("Read Channel"))
  file.write(port("rd_addr", "output", width="ADDR_WIDTH", tabs=1))
  file.write(port("rd_data",  "input", width="DATA_WIDTH", tabs=1))
  file.write(port("rd_en",   "output", width=1, tabs=1))

  file.write(");\n\n")

def _write_sram_local_params(file:TextIOWrapper, mem_map:dict) :
  """Writes the local params required for the SRAM bank

  Args:
      file (TextIOWrapper): The writable file to output the SRAM bank to
      mem_map (dict): The memory map definition for the SRAM bank
  """

  file.write(comment_block(f"Local Params", tabs=1))

  for reg in mem_map["registers"] :
    file.write(localparam(f"{reg['name'].upper()}_ADDR", default=f"{hex(reg['offset'])};\n".replace('0x', '\'h'), tabs=1))
  
  file.write("\n")
