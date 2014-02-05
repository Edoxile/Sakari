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
from modules.Module import Module, get_target, Command
import random
import string
from urllib import request

__author__ = 'windwarrior, Edoxile'


class Random(Module):
    @Command('random', 'r')
    def random(self, c, e, args):
        try:
            for i in range(len(args)):
                current = args[i]
                args[i] = int(current)
        except ValueError as e:
            c.privmsg(get_target(c, e), "")

        if len(args) == 1:
            val = random.randint(0, args[0])
        elif len(args) == 2:
            if args[0] > args[1]:
                (args[0], args[1]) = (args[1], args[0])
            val = random.randint(args[0], args[1])
        c.privmsg(get_target(c, e), 'I choose \x02{}\x0f!'.format(val))

    @Command('choose', 'c')
    def choose(self, c, e, args):
        if not len(args) > 0:
            c.privmsg(get_target(c, e), 'I need arguments to choose from!')
        else:
            ch = random.choice(args)
            c.privmsg(get_target(c, e), 'I choose \x02{}\x0f!'.format(ch))

    @Command('ri', 'randomi', 'rimigur', 'randomimigur')
    def imgur(self, c, e, args):
        while True:
            url = 'http://i.imgur.com/' + ''.join(random.sample(string.ascii_letters + string.digits, 5)) + '.png'
            r = request.urlopen(url)
            if r.geturl() != 'http://i.imgur.com/removed.png':
                c.privmsg(get_target(c, e), 'Random Imgur (might be NSFW!): {}'.format(url))
                break