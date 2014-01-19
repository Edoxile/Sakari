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
from modules.AuthModule import AuthModule, get_target
from exceptions import SakariException

import itertools
import threading

__author__ = 'Edoxile'


class Manage(AuthModule):
    def get_hooks(self):
        return [
            ('list', self.list),
            ('reload', self.reload),
            ('load', self.load),
            ('unload', self.unload),
            ('join', self.join),
            ('part', self.part),
            ('die', self.die)
        ]

    def die(self, c, e, args):
        self.bot.die()

    def reload(self, c, e, args):
        modules = itertools.chain.from_iterable([n.split(',') for n in args])
        for m in modules:
            try:
                self.bot.unload_module(m)
                self.bot.load_module(m)
                c.privmsg(get_target(c, e), "\x02{}\x0f reloaded successfully!".format(m))
            except SakariException as ex:
                c.privmsg(get_target(c, e), "Couldn't reload \x02{}\x0f: %s".format(m, ex.error))

    def load(self, c, e, args):
        modules = itertools.chain.from_iterable([n.split(',') for n in args])
        for m in modules:
            try:
                print(threading.current_thread())
                self.bot.load_module(m)
                c.privmsg(get_target(c, e), "\x02{}\x0f loaded successfully!".format(m))
            except SakariException as ex:
                c.privmsg(get_target(c, e), "Couldn't load \x02{}\x0f: {}".format((m, ex.error)))

    def unload(self, c, e, args):
        modules = itertools.chain.from_iterable([n.split(',') for n in args])
        for m in modules:
            try:
                self.bot.unload_module(m)
                c.privmsg(get_target(c, e), "\x02{}\x0f unloaded successfully!".format(m))
            except SakariException as ex:
                c.privmsg(get_target(c, e), "Couldn't unload \x02{}\x0f: {}".format(m, ex.error))

    def join(self, c, e, args):
        pass

    def part(self, c, e, args):
        pass

    def list(self, c, e, args):
        if len(args) and args[0] == 'modules':
            ms = self.bot.modules.values()
            response = "\x02Active:\x0f " + ", ".join(x.get_name() for x in ms if x.active)
            response += ". \x02Inactive:\x0f " + ", ".join(x.get_name() for x in ms if not x.active)
            c.privmsg(get_target(c, e), response)
