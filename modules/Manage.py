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
from subprocess import check_output, CalledProcessError
import itertools
from modules.Module import Command

__author__ = 'Edoxile, windwarrior'


class Manage(AuthModule):
    @Command('die')
    def die(self, c, e, args):
        if not self.is_authorized(c, e, 5):
            c.privmsg(get_target(c, e), "You don't have permission to let me die!")
            return
        self.bot.die()

    @Command('reload')
    def reload(self, c, e, args):
        if not self.is_authorized(c, e, 5):
            c.privmsg(get_target(c, e), "You don't have permission to reload modules!")
            return
        modules = itertools.chain.from_iterable([n.split(',') for n in args])
        for m in modules:
            try:
                self.bot.unload_module(m)
                self.bot.load_module(m)
                c.privmsg(get_target(c, e), '\x02{}\x0f reloaded successfully!'.format(m))
            except SakariException as ex:
                c.privmsg(get_target(c, e), "Couldn't reload \x02{}\x0f: %s".format(m, ex.error))

    @Command('load')
    def load(self, c, e, args):
        if not self.is_authorized(c, e, 5):
            c.privmsg(get_target(c, e), "You don't have permission to load modules!")
            return
        modules = itertools.chain.from_iterable([n.split(',') for n in args])
        for m in modules:
            try:
                self.bot.load_module(m)
                c.privmsg(get_target(c, e), '\x02{}\x0f loaded successfully!'.format(m))
            except SakariException as ex:
                c.privmsg(get_target(c, e), "Couldn't load \x02{}\x0f: {}".format(m, ex.error))

    @Command('unload')
    def unload(self, c, e, args):
        if not self.is_authorized(c, e, 5):
            c.privmsg(get_target(c, e), "You don't have permission to unload modules!")
            return
        modules = itertools.chain.from_iterable([n.split(',') for n in args])
        for m in modules:
            try:
                self.bot.unload_module(m)
                c.privmsg(get_target(c, e), '\x02{}\x0f unloaded successfully!'.format(m))
            except SakariException as ex:
                c.privmsg(get_target(c, e), "Couldn't unload \x02{}\x0f: {}".format(m, ex.error))

    @Command('join')
    def join(self, c, e, args):
        print('Joining channels {}.'.format(args[0].split(',')))
        for ch in args[0].split(','):
            c.join(ch)

    @Command('part')
    def part(self, c, e, args):
        if len(args) > 0:
            print('Parting channels {}.'.format(args[0].split(',')))
            for ch in args[0].split(','):
                c.part(ch, ' '.join(args[1:]))
        else:
            c.part(e.target)

    @Command('list')
    def list(self, c, e, args):
        if len(args) and args[0] == 'modules':
            ms = self.bot.modules.values()
            response = '\x02Active:\x0f ' + ', '.join(x.get_name() for x in ms if x.active)
            response += '. \x02Inactive:\x0f ' + ', '.join(x.get_name() for x in ms if not x.active)
            c.privmsg(get_target(c, e), response)
        elif len(args) and args[0] == 'channels':
            c.privmsg(get_target(c, e), '\x02Channels:\x0f ' + ', '.join(self.bot.channels.keys()) + '.')

    @Command('update')
    def update(self, c, e, args):
        if not self.is_authorized(c, e, 5):
            c.privmsg(get_target(c, e), "You don't have permission to update!")
            return
        try:
            response = check_output(['git', 'pull'])
            for msg in response.decode('utf-8').split("\n"):
                c.privmsg(get_target(c, e), msg)
        except CalledProcessError as ex:
            c.privmsg(get_target(c, e), "Error on calling 'git pull': {}".format(ex.output))