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

import r2x

bank = r2x.bank_from_file("sample_bank.csv")

# tbl = [["bank","name","sample_bank"],
#        ["bank","reg_width","64"],
#        ["bank","bus_type","axi4"],
#        ["register","version","ro"],
#        ["field","major","8","ro","0"],
#        ["field","minor","8","ro","0"],
#        ["field","patch","8","ro","0x1"]]

# bank = r2x.bank_from_table(tbl)

print(bank)