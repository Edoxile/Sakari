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
from sakari import SakariException

__author__ = 'Edoxile'


class Manage(Module):
    def get_hooks(self):
        return [
            ('list', self.list),
            ('load', self.load),
            ('unload', self.unload),
            ('join', self.join),
            ('part', self.part),
            ('die', self.die)
        ]

    def die(self, c, e, args):
        self.bot.die()

    def load(self, c, e, args):
        modules = [n.split(',') for n in args]
        for m in modules:
            try:
                self.bot.load_module(m)
                c.privmsg(e.target, "\x02%s\x00 loaded successfully!" % m)
            except SakariException as ex:
                c.privmsg(e.target, "Couldn't load \x02%s\x00: %s" % (m, ex.error))

    def unload(self, c, e, args):
        modules = [n.split(',') for n in args]
        for m in modules:
            try:
                self.bot.unload_module(m)
                c.privmsg(e.target, "\x02%s\x00 unloaded successfully!" % m)
            except SakariException as ex:
                c.privmsg(e.target, "Couldn't unload \x02%s\x00: %s" % (m, ex.error))

    def join(self, c, e, args):
        c.join(args[0])

    def part(self, c, e, args):
        c.part(args[0])

    def list(self, c, e, args):
        if args[0] == 'modules':
            ms = self.bot.modules.values()
            response = "\x02Active:\x0F " + ", ".join(x.get_name() for x in ms if x.active)
            response += ". \x02Inactive:\x0F " + ", ".join(x.get_name() for x in ms if not x.active)
            c.privmsg(e.target, response)