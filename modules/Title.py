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
from modules.Module import Module
import re

__author__ = 'Edoxile'


class Title(Module):

    def __init__(self, b):
        super().__init__(b)
        self.re_title = re.compile("((?:https?://|www\.)[-~=\\\/a-zA-Z0-9\.:_\?&%,#\+]+)")

    def get_commands(self):
        return []

    def get_hooks(self):
        return [
            ('privmsg', self.get_title)
        ]

    def get_title(self, c, e, msg):
        m = self.re_title.match(msg)
        return
        if m:
            pass
