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
    def __init__(self, b):
        self.bot = b
        self.active = False
        print('Module ' + self.get_name() + ' loaded successfully!')

    def __new__(mcls, bot):
        cls = super().__new__(mcls)
        cls.commands = []
        cls.hooks = dict()
        for name in mcls.__dict__.keys():
            fnc = mcls.__dict__[name]
            if getattr(fnc, '__has_commands__', False):
                cls.commands.append((fnc, fnc.__commands__))
            if getattr(fnc, '__has_hooks__', False):
                for hk in fnc.__hooks__:
                    if hk not in cls.hooks.keys():
                        cls.hooks[hk] = [fnc]
                    else:
                        cls.hooks[hk].append(fnc)
        return cls

    def get_commands(self):
        return self.commands

    def get_hooks(self):
        return self.hooks

    def get_name(self):
        return self.__class__.__name__


class Command(object):
    def __init__(self, *cmds):
        self.commands = list(cmds)

    def __call__(self, f):
        f.__has_commands__ = True
        f.__commands__ = self.commands
        return f


class Hook(object):
    def __init__(self, *hks):
        self.hooks = list(hks)

    def __call__(self, f):
        f.__has_hooks__ = True
        f.__hooks__ = self.hooks
        return f


def get_target(c, e):
    return e.source.nick if e.target == c.get_nickname() else e.target