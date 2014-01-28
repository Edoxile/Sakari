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
from modules.Module import Module, get_target
import wikipedia
from wikipedia.exceptions import DisambiguationError

__author__ = 'Edoxile'


class Wiki(Module):
    def __init__(self, b):
        super().__init__(b)
        wikipedia.set_lang(self.bot.config.get('wikipedia', 'lang'))

    def get_commands(self):
        return [
            ('w', self.search),
            ('rw', self.random),
            ('wl', self.search_lang)
        ]

    def get_hooks(self):
        return []

    def search_lang(self, c, e, args):
        wikipedia.set_lang(args[0])
        p = wikipedia.page(' '.join(args[1:]))
        if p:
            c.privmsg(get_target(c, e), '\x02{}\x0f - {} [ {} ]'.format(p.title, smart_truncate(p.summary), p.url))
        wikipedia.set_lang(self.bot.config.get('wikipedia', 'lang'))

    def search(self, c, e, args):
        p = wikipedia.page(' '.join(args))
        if p:
            c.privmsg(get_target(c, e), '\x02{}\x0f - {} [ {} ]'.format(p.title, smart_truncate(p.summary), p.url))

    def random(self, c, e, args):
        while True:
            try:
                p = wikipedia.page(wikipedia.random())
                if p:
                    c.privmsg(get_target(c, e), '\x02{}\x0f - {} [ {} ]'.format(p.title, smart_truncate(p.summary), p.url))
                    break
            except DisambiguationError:
                pass


def smart_truncate(content, length=200, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0] + suffix