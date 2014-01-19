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
from modules.Module import Module, get_target

__author__ = 'Edoxile'


class Test(Module):
    def get_commands(self):
        return [
            ('test', self.test),
            ('ntest', self.ntest),
            ('raw', self.raw),
            ('blub', self.blub)
        ]

    def test(self, c, e, args):
        c.privmsg(get_target(c, e), "Test called successfully! Args: {}".format(args))

    def ntest(self, c, e, args):
        c.notice(e.source.nick, "Test called successfully! Args: {}".format(args))

    def raw(self, c, e, args):
        print("Sending raw command: '{}'".format(" ".join(args)))
        c.send_raw(" ".join(args))

    def blub(self, c, e, args):
        c.privmsg(get_target(c, e), "blab")