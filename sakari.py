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

__author__ = 'Edoxile'

import ssl
import irc.bot
import irc.connection
from modules.Module import Module
from configparser import ConfigParser


class SakariException(Exception):
    def __init__(self, error, data=None):
        self.error = error
        self.data = data

    def __str__(self):
        return repr(self.error)


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
        self.commands = {}
        self.modules = {}
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
            self.do_command(e, a[0][1:], a[1:])
        return

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(" ")
        if len(a[0]) > 1 and a[0][0] == '~':
            self.do_command(e, a[0][1:], a[1:])
        return

    def do_command(self, e, cmd, args):
        c = self.connection

        if cmd in self.commands.keys():
            (m, f) = self.commands[cmd]
            f(c, e, args)

    def load_module(self, mn):
        if mn in self.modules.keys():
            if not self.modules[mn].active:
                self._register_commands(self.modules[mn])
                self.modules[mn].active = True
            else:
                raise SakariException("Module %s already loaded!" % mn)
        else:
            try:
                mod = __import__('modules.' + mn, fromlist=[mn])
            except ImportError:
                raise SakariException("Tried importing a module that does not exist {}".format(mn))
            clazz = getattr(mod, mn)
            m = clazz(self)
            if not isinstance(m, Module):
                raise SakariException("Object given to load_module, but object is not an instance of Module")
            else:
                dupe = self._register_commands(m)
                if dupe:
                    raise SakariException("Duplicate command list found when loading module %s. Commands: {%s}" % (
                        m.get_name(), ", ".join(dupe)))
                else:
                    m.active = True
                    self.modules.update({mn: m})

    def unload_module(self, mn):
        if mn in self.modules.keys():
            self._remove_commands(self.modules[mn])
            self.modules[mn].active = False
        else:
            raise SakariException("Module %s is not yet loaded!" % mn)

    def get_module(self, mn):
        if mn in self.modules.keys():
            return self.modules[mn]
        else:
            raise SakariException("Module %s not loaded!" % mn)

    @staticmethod
    def _mod_import(name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def _register_commands(self, m):
        #check if hooks are available
        dupe = [i for i in [n[0] for n in m.get_hooks()] if i in self.commands.keys()]
        if dupe:
            return dupe
        else:
            for (c, f) in m.get_hooks():
                self.commands.update({c: (m, f)})
            return []

    def _remove_commands(self, m, hooks=None):
        if hooks is None:
            hooks = m.get_hooks
        for (c, f) in hooks:
            del self.commands[c]       


if __name__ == "__main__":
    sakari = Sakari()

    try:
        sakari.start()
    except KeyboardInterrupt:
        sakari.die("Killed by Ctrl+C")
