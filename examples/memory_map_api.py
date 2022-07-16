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

import json
import r2x.memory_map as memmap

bank = memmap.AddressBank("ExampleBank", memmap.AccessType.RW, offset=0, regSize=32)

reg = memmap.Register("version", memmap.AccessType.RO, offset=0, reserved=False)
reg.add_field(memmap.Field("patch", memmap.AccessType.RO, offset=0, width=8, reset=0x0))
reg.add_field(memmap.Field("minor", memmap.AccessType.RO, offset=8, width=8, reset=0x2))
reg.add_field(memmap.Field("major", memmap.AccessType.RO, offset=16, width=8, reset=0x1))
bank.add_register(reg)

reg = memmap.Register("control", accessType=memmap.AccessType.RW, offset=4)
reg.add_field(memmap.Field("start", memmap.AccessType.RW, offset=0, width=1, reset=0x0))
reg.add_field(memmap.Field("timeout_cnt", memmap.AccessType.RW, offset=1, width=8, reset=0xF))
bank.add_register(reg)

reg = memmap.Register("status", accessType=memmap.AccessType.RO, offset=bank._current_size, volatile=True)
reg.add_field(memmap.Field("running", memmap.AccessType.RO, offset=0, width=1, reset=0x0))
reg.add_field(memmap.Field("ready", memmap.AccessType.RO, offset=1, width=1, reset=0x0))
reg.add_field(memmap.Field("timeout", memmap.AccessType.RO, offset=2, width=1, reset=0x0))

map = memmap.MemoryMap("ExampleMap")
map.add_bank(bank)

print(json.dumps(map.to_dict(), indent=2))
