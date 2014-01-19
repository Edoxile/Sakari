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

__author__ = 'windwarrior'


class Choose(Module):
    def get_hooks(self):
        return [
            ('random', self.random),
            ('choose', self.choose)
        ]

    def random(self, c, e, args):
        args = [int(n) for n in args]
        if len(args) == 1:
            val = random.randint(0, args[0])
        elif len(args) == 2:
            if args[0] > args[1]:
                (args[0], args[1]) = (args[1], args[0])
            val = random.randint(args[0], args[1])
        c.privmsg(get_target(c, e), "I choose \x02{}\x0f!".format(val))

    def choose(self, c, e, args):
        pass

    def get_name(self):
        return self.__class__.__name__