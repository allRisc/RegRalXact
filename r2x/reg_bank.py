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
from r2x.system_verilog import *

def _write_reg_ports(file:TextIOWrapper, mem_map:dict) :
  """Writes register ports into the module definition based on the memory map

  Args:
      file (TextIOWrapper): The writable file to output the SRAM bank to
      mem_map (dict): The memory map definition for the SRAM bank
  """
  file.write(comment_block("Register Bank Signals", tabs=1, mod=True))

  for reg in mem_map['register'] :
    file.write(comment(f"{reg['name']} Register"))

    if "properties" in reg :
      if "write_trigger" in reg["properties"] :
        file.write(port(f"{reg['name']}_write_trigger", "output", tabs=1))
      if "read_trigger" in reg["properties"] :
        file.write(port(f"{reg['name']}_read_trigger", "output", tabs=1))

    for fld in reg['fields'] :
      _write_fld_ports(file, fld, reg['name'])


def _write_fld_ports(file:TextIOWrapper, fld:dict, reg_name:str) :
  """Writes a field port into the module definition from the provided fld definition and register name

  Args:s
      file (TextIOWrapper): The writable file to output the SRAM bank to
      fld (dict): The field definition
      reg_name (str): The name of the register which the field belongs to
  """
  if "reserved" in fld and fld['reserved'] :
    return

  dir = "input" if fld['access'] == "RO" else "output"
  file.write(port(f"{reg_name}_{fld['name']}", dir, fld['width'], tabs=1))

  if "properties" in fld :
    if "write_trigger" in fld["properties"] :
      file.write(port(f"{reg_name}_{fld['name']}_write_trigger", "output", tabs=1))
    if "read_trigger" in fld["properties"] :
      file.write(port(f"{reg_name}_{fld['name']}_read_trigger", "output", tabs=1))