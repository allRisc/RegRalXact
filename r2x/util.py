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
""" A set of useful method definitions for the r2x package """

def value2hex(v:str, length:int=None) -> str :
    """Converts the provided string value to a hex representation without prefix"""

    v = v.lower()

    # Try a straight conversion to integer
    try :
        h = int(v)
        rval = hex(h)[2:]
    except :
        rval = None

    if not rval is None :
        pass

    # Check if the string is provided as a hex
    elif (v.startswith("0x")) :
        rval = v[2:]
    elif (v.startswith("h")) :
        rval = v[1:]
    elif (v.startswith("'h")) :
        rval = v[2:]
    
    # Pad the hex if necessary and return
    if length is None :
        return rval
    elif length > len(rval) :
        return ('0' * (length - len(rval))) + rval
    else :
        return rval[(len(rval)-length):]
