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

from r2x.util import *

import unittest
import random


class TestUtil (unittest.TestCase) :
    """Unit Test Cases for Methods in the r2x.util module"""

    def test_value2hex (self) :
        """Tests the functionality of the value2hex method"""

        self.assertEqual("a", value2hex("10"), "Check that integers get converted properly (10)")
        self.assertEqual("2b", value2hex("43"), "Check that integers get converted properly (43)")

        self.assertEqual("a", value2hex("0xA"), "Check the default hex prefixes work")
        self.assertEqual("a", value2hex("hA"), "Check the default hex prefixes work")
        self.assertEqual("a", value2hex("'hA"), "Check the default hex prefixes work")