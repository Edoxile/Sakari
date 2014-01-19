#!/usr/bin/python

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
import random
from modules.Module import Module, get_target

__author__ = 'windwarrior, Edoxile'


class Choose(Module):
    def get_hooks(self):
        return [
            ('random', self.random),
            ('choose', self.choose)
        ]

    def random(self, c, e, args):
        current = args[0]
        try:
            for n in range(len(args)):
                current = args[n]
                args[n] = int(current)
        except ValueError:
            c.privmsg(get_target(c,e), "\x02{}\x0f is no number!".format(current))
            return

        if 0 < len(args) <= 2: 
            if len(args) == 1:
                args.append(0)
            if args[0] > args[1]:
                (args[0], args[1]) = (args[1], args[0])
            val = random.randint(args[0], args[1])
            c.privmsg(get_target(c, e), "I choose \x02{}\x0f!".format(val))
        else:
            c.privmsg(get_target(c, e), "Usage: \x02random\0xf <x> [y]")

    def choose(self, c, e, args):
        if len(args) > 0:
            c.privmsg(get_target(c, e), "I choose \x02{}\x0f!".format(random.choice(args)))
        else:
            c.privmsg(get_target(c, e), "Usage: \x02choose\0xf [x..]")
