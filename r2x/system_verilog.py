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

def comment(comment:str, tabs:int=0) :
  return "  " * tabs + f"// {comment}\n"

def comment_block(comment:str, tabs:int=0, mod:bool=False) :
  rstr += "  " * tabs + "/" * 70 + "\n"
  rstr += comment(comment, tabs)
  if not mod :
    rstr += "  " * tabs + "/" * 70 + "\n"
  else :
    rstr += "  " * tabs + "//" + "=" * 68 + "\n"

  return rstr

def parameter(name:str, default=None, ptype=None, tabs:int=0) :
  rstr = "  " * tabs + f"parameter "
  if not ptype is None :
    rstr += f"{ptype} "

  rstr += f"{name}"

  if not default is None :
    rstr += f" = {default}"

  return rstr + ";\n"

def localparam(name:str, default, ptype=None, tabs:int=0) :
  rstr = "  " * tabs + f"localparam"
  if not ptype is None :
    rstr += f"{ptype} "

  rstr += f"{name} = {default}"

  return rstr + ";\n"

def port(name:str, dir:str, width=0, tabs:int=0) :
  rstr = "  " * tabs + f"{dir} "
  if isinstance(width, str) :
    rstr += f"[{width}-1:0] "
  elif width > 1 :
    rstr += f"[{width-1}:0] "
  rstr += f"{name}_in,\n" if dir == "input" else f"{name}_out,\n"
  return rstr

def assign(lhs:str, rhs:str, tabs:int=0) :
  return "  " * tabs + f"assign {lhs} = {rhs};\n"
