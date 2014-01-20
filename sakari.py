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

        factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        irc.bot.SingleServerIRCBot.__init__(
            self, [(self.config.get("server", "host"), int(self.config.get("server", "port")))],
            self.config.get("server", "username"), self.config.get("server", "realname"), 60, connect_factory=factory
        )
        self.channel = self.config.get("server", "channel")
        self.prefix = self.config.get("bot", "command_prefix")
        self.commands = dict()
        self.modules = dict()
        self.hooks = {
            'on_privmsg': [], 'on_pubmsg': [], 'on_error': [], 'on_join': [], 'on_kick': [], 'on_mode': [],
            'on_part': [], 'on_privnotice': [], 'on_pubnotice': [], 'on_quit': [], 'on_invite': [], 'on_action': [],
            'on_topic': [], 'on_nick': []
        }
        for m in self.config.get("bot", "default_modules").split(","):
            try:
                self.load_module(m)
            except SakariException as ex:
                print(ex.error)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        a = e.arguments[0].split(" ")
        if len(a[0]) > 1 and a[0][0] == '~':
            self._run_command(c, e, a[0][1:], a[1:])
        self._run_hook('on_privmsg', c, e)

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(" ")
        if len(a[0]) > 1 and a[0][0] == '~':
            self._run_command(c, e, a[0][1:], a[1:])
        self._run_hook('on_pubmsg', c, e)

    def on_error(self, c, e):
        self._run_hook('on_error', c, e)

    def on_join(self, c, e):
        self._run_hook('on_join', c, e)

    def on_kick(self, c, e):
        self._run_hook('on_kick', c, e)

    def on_mode(self, c, e):
        self._run_hook('on_mode', c, e)

    def on_part(self, c, e):
        self._run_hook('on_part', c, e)

    def on_privnotice(self, c, e):
        self._run_hook('on_privnotice', c, e)

    def on_pubbnotice(self, c, e):
        self._run_hook('on_pubnotice', c, e)

    def on_quit(self, c, e):
        self._run_hook('on_quit', c, e)

    def on_invite(self, c, e):
        self._run_hook('on_invite', c, e)

    def on_action(self, c, e):
        self._run_hook('on_action', c, e)

    def on_topic(self, c, e):
        self._run_hook('on_topic', c, e)

    def on_nick(self, c, e):
        self._run_hook('on_nick', c, e)

    def load_module(self, mn):
        if mn in self.modules.keys():
            if not self.modules[mn].active:
                mod = reload(sys.modules[self.modules[mn].__module__])
            else:
                raise SakariException("Module {} already loaded!".format(mn))
        else:
            try:
                mod = import_module('modules.' + mn)
            except ImportError:
                raise SakariException("Tried importing a module that does not exist {}".format(mn))
        clazz = getattr(mod, mn)
        m = clazz(self)
        if not isinstance(m, Module):
            raise SakariException("Object given to load_module, but object is not an instance of Module")
        else:
            dupe = self._register_commands(m)
            if dupe:
                raise SakariException("Duplicate command list found when loading module {}. Commands: {}".format(
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
            raise SakariException("Module {} is not yet loaded!".format(mn))

    def get_module(self, mn):
        if mn in self.modules.keys():
            return self.modules[mn]
        else:
            raise SakariException("Module {} not loaded!".format(mn))

    def _run_hook(self, hook, c, e):
        for f in self.hooks[hook]:
            f(c, e, e.arguments[0])

    def _run_command(self, c, e, cmd, args):
        if cmd in self.commands.keys():
            (m, f) = self.commands[cmd]
            f(c, e, args)

    @staticmethod
    def _mod_import(name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def _register_commands(self, m):
        dupe = [i for i in [n[0] for n in m.get_commands()] if i in self.commands.keys()]
        if dupe:
            return dupe
        else:
            for (c, f) in m.get_commands():
                self.commands.update({c: (m, f)})
            return []

    def _remove_commands(self, m, cmds=None):
        if not cmds:
            cmds = m.get_commands()
        for (c, f) in cmds:
            del self.commands[c]

    def _register_hooks(self, m):
        if m.get_hooks():
            for (h, f) in m.get_hooks():
                self.hooks[h].extend(f)

    def _remove_hooks(self, m, hks=None):
        if not hks:
            if m.get_hooks():
                hks = m.get_hooks()
            else:
                return
        for (h, f) in hks:
            self.hooks[h].remove(f)


if __name__ == "__main__":
    sakari = Sakari()
    try:
        sakari.start()
    except KeyboardInterrupt:
        sakari.die("Killed by Ctrl+C")