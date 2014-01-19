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
from exceptions import SakariException
from modules.Module import Module, get_target
from abc import ABCMeta, abstractmethod

__author__ = 'Edoxile'


class AuthModule(Module):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_hooks(self):
        super().get_hooks()

    def get_auth_level(self, c, e):
        try:
            auth = self.bot.get_module('Auth')
            return auth.get_level(c, e)
        except SakariException as ex:
            c.privmsg(get_target(c, e), "Couldn't fetch auth level. Error: {}".format(ex.error))
            return None

    def is_authorized(self, c, e, r):
        level = self.get_auth_level(c, e)
        if level is not None:
            return level >= r
        else:
            return False