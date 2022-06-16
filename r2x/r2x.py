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
""" Module which contains the base-level API for the r2x pacakge """

import math

import pandas as pd

from r2x.bank import *
from r2x.util import *


import os

DEFAULT_BANK_NAME = "default_bank"
DEFAULT_BANK_WIDTH = 32
DEFAULT_BANK_BUS = BusInterface.SRAM


def _fld_from_row(row:list) -> Field :
    name = row[1]
    width = row[2]
    access = str2access(row[3])

    try :
        width = int(width)
    except :
        raise ValueError("Field width (column C) must be integer")

    if (len(row) > 4 and not row[4] is None) :
        rst = value2hex(row[4], math.ceil(width / 4))
    else :
        rst = "0" * math.ceil(width / 4)

    fld = Field(name, width, access, rst)
    
    return fld

def bank_from_table(tbl:list) -> Bank:
    
    # Process initial bank settings from tbl
    name = DEFAULT_BANK_NAME
    width = DEFAULT_BANK_WIDTH
    bus = DEFAULT_BANK_BUS

    for row in tbl :
        if row[0] != 'bank' :
            continue
        if row[1] == 'name' :
            name = row[2]
        elif row[1] == 'bus' or row[1] == 'bus_type' :
            bus = str2bus(row[2])
        elif row[1] == 'width' or row[1] == 'reg_width' :
            width = int(row[2])

    bnk = Bank(name, bus, width)
    
    # Handle the registers
    reg = None
    fld = None

    for row in tbl :
        if row[0] == 'register' :
            if (not reg is None) :
                if (not fld is None) :
                    reg.add_field(fld)
                    fld = None
                bnk.add_register(reg)
            reg = Register(row[1], str2access(row[2]))
        elif row[0] == 'field' :
            if (not fld is None) :
                reg.add_field(fld)
            fld = _fld_from_row(row)

    if (not fld is None) :
        reg.add_field(fld)
    if (not reg is None) :
        bnk.add_register(reg)
 
    return bnk

def bank_from_file(filename:str) -> Bank :

    if (not os.path.exists(filename)) :
        raise ValueError(f"Filename ({filename}) does not exist to create bank from")

    print(filename)

    if filename.endswith(".csv") :
        tbl = pd.read_csv(filename, header=None).values
    elif filename.endswith(".xls") :
        tbl = pd.read_excel(filename, header=None).values
    elif filename.endswith(".xlsx") :
        tbl = pd.read_excel(filename, header=None).values
    else :
        raise ValueError("r2x Currently Only Supports Bank Creation from Excel and CSV files")

    return bank_from_table(tbl)


def parse_rtl_file(filename:str) :
    if (not os.path.exists(filename)) :
        raise ValueError(f"Filename ({filename}) does not exist to parse rtl from")
    
    with open(filename, "r") as f :
        rtl = f.read()

    print(rtl)

    if (filename.endswith(".sv")) :
        return sverilog.to_design(rtl)
    elif (filename.endswith(".v")) :
        return verilog.to_design(rtl)
    elif (filename.endswith(".vhd") or filename.endswith(".vhdl")) :
        raise NotImplementedError("Parsing of VHDL files is not currently implemented")
    else :
        raise ValueError(f"The RTL file '{filename}' has an unknown extension")