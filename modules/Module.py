# Copyright (c) 2014.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
from abc import ABCMeta, abstractmethod

__author__ = 'Edoxile'


class Module:
    __metaclass__ = ABCMeta

    def __init__(self, b):
        self.bot = b
        print('Module ' + self.get_name() + ' loaded successfully!')
        self.active = False

    @abstractmethod
    def get_commands(self):
        pass

    @abstractmethod
    def get_hooks(self):
        pass

    def get_name(self):
        return self.__class__.__name__


def get_target(c, e):
    return e.source.nick if e.target == c.get_nickname() else e.target