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
from imp import reload
import ssl
import irc.bot
import irc.connection
import sys
import sqlite3
from modules.Module import Module
from configparser import ConfigParser
from exceptions import SakariException

try:
    from importlib import import_module
except ImportError:
    import_module = __import__

__author__ = 'Edoxile, windwarrior'


class Sakari(irc.bot.SingleServerIRCBot):
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('sakari.cfg')
        self.hooks = {
            'privmsg': [], 'pubmsg': [], 'error': [], 'join': [], 'kick': [], 'mode': [], 'part': [], 'privnotice': [],
            'pubnotice': [], 'quit': [], 'invite': [], 'action': [], 'topic': [], 'nick': []
        }
        for h in self.hooks.keys():
            if h != 'privmsg' and h != 'pubmsg':
                setattr(Sakari, 'on_' + h, self.__pass_event)

        factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        irc.bot.SingleServerIRCBot.__init__(
            self, [(self.config.get('server', 'host'), int(self.config.get('server', 'port')))],
            self.config.get('server', 'username'), self.config.get('server', 'realname'), 60, connect_factory=factory
        )
        self.channel = self.config.get('server', 'channel')
        self.prefix = self.config.get('bot', 'command_prefix')
        self.commands = dict()
        self.modules = dict()
        self.database = sqlite3.connect('sakari.sqlite')
        for m in self.config.get('bot', 'default_modules').split(','):
            try:
                self.load_module(m)
            except SakariException as ex:
                print(ex.error)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + '_')

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        a = e.arguments[0].split(' ')
        if len(a[0]) > 1 and a[0][0] == self.prefix:
            self._run_command(c, e, a[0][1:], a[1:])
        self.__pass_event(c, e)

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(' ')
        if len(a[0]) > 1 and a[0][0] == self.prefix:
            self._run_command(c, e, a[0][1:], a[1:])
        self.__pass_event(c, e)

    def load_module(self, mn):
        if mn in self.modules.keys():
            if not self.modules[mn].active:
                mod = reload(sys.modules[self.modules[mn].__module__])
            else:
                raise SakariException('Module {} already loaded!'.format(mn))
        else:
            try:
                mod = import_module('modules.' + mn)
            except ImportError as ie:
                raise SakariException('Tried importing a module but it failed: {}'.format(ie.msg))
        clazz = getattr(mod, mn)
        m = clazz(self)
        if not isinstance(m, Module):
            raise SakariException('Object given to load_module, but object is not an instance of Module')
        else:
            dupe = self._register_commands(m)
            if dupe:
                raise SakariException('Duplicate command list found when loading module {}. Commands: {}'.format(
                    m.get_name(), dupe))
            else:
                m.active = True
                self.modules.update({mn: m})
                self._register_hooks(m)

    def unload_module(self, mn):
        if mn in self.modules.keys():
            self._remove_commands(self.modules[mn])
            self._remove_hooks(self.modules[mn])
            self.modules[mn].active = False
        else:
            raise SakariException('Module {} is not yet loaded!'.format(mn))

    def get_module(self, mn):
        if mn in self.modules.keys():
            return self.modules[mn]
        else:
            raise SakariException('Module {} not loaded!'.format(mn))

    def _run_hook(self, hook, c, e):
        for d in self.hooks[hook]:
            for m in d.keys():
                [f(m, c, e) for f in d[m]]

    def _run_command(self, c, e, cmd, args):
        if cmd in self.commands.keys():
            (m, f) = self.commands[cmd]
            f(m, c, e, args)

    @staticmethod
    def _mod_import(name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def _register_commands(self, m):
        dupe = [i for n in m.get_commands() for i in n[1] if i in self.commands.keys()]
        if dupe:
            return dupe
        else:
            for (f, cmds) in m.get_commands():
                for cmd in cmds:
                    self.commands.update({cmd: (m, f)})
            return []

    def _remove_commands(self, m):
        for cmd in [n for (f, n) in m.get_commands()]:
            del self.commands[cmd]

    def _register_hooks(self, m):
        if m.get_hooks():
            for h in [n for n in self.hooks if n in m.get_hooks().keys()]:
                self.hooks[h].append({m: m.get_hooks()[h]})

    def _remove_hooks(self, m):
        for h in [n for n in self.hooks if n in m.get_hooks().keys()]:
            del self.hooks[h][m]

    def __pass_event(self, c, e):
        self._run_hook(e.type, c, e)


if __name__ == '__main__':
    sakari = Sakari()
    try:
        sakari.start()
    except KeyboardInterrupt:
        sakari.die('Killed by Ctrl+C')