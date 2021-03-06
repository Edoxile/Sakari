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
from modules.Module import Module, get_target, Hook
import re

__author__ = 'Edoxile'


class Quote(Module):
    def __init__(self, bot):
        super().__init__(bot)
        self.buffer = dict()
        self.re_quote = re.compile('^(\w{1,2})/((?:(?:.+?)(?:\\\/)*)+?)/(?:((?:(?:.+?)(?:\\\/)*)+?)/)*(\w*)')
        self.quote_commands = {
            'q': self.quote,
            's': self.subs,
            #'sd': self.subswitch,
            #'qu': self.quote_user
        }

    @Hook('pubmsg')
    def handle_msg(self, c, e):
        msg = e.arguments[0]
        m = self.re_quote.match(msg)
        if m:
            if get_target(c, e) in self.buffer.keys() and m.group(1) in self.quote_commands.keys():
                msg = self.quote_commands[m.group(1)](get_target(c, e), m)
                if msg:
                    c.privmsg(get_target(c, e), msg)
        else:
            if get_target(c, e) in self.buffer.keys():
                self.buffer[get_target(c, e)] = [(e.source.nick, msg)] + self.buffer[get_target(c, e)]
                if len(self.buffer[get_target(c, e)]) > 100:
                    self.buffer[get_target(c, e)] = self.buffer[get_target(c, e)][:100]
            else:
                self.buffer.update({get_target(c, e): [(e.source.nick, msg)]})

    def quote(self, ch, m):
        if ch not in self.buffer.keys():
            return None
        if 'i' in m.group(4):
            qre = re.compile(m.group(2), flags=re.IGNORECASE)
        else:
            qre = re.compile(m.group(2))
        for (n, msg) in self.buffer[ch]:
            q = qre.search(msg)
            if q:
                return "<{}> {}".format(n, msg)
        return None

    def subs(self, ch, m):
        if ch not in self.buffer.keys():
            return None
        if m.group(4) is not None and 'i' in m.group(4):
            sre = re.compile(m.group(2), flags=re.IGNORECASE)
        else:
            sre = re.compile(m.group(2))
        for (n, msg) in self.buffer[ch]:
            s = sre.search(msg)
            if s and m.group(4) is not None and not 'g' in m.group(4):
                return "<{}> {}".format(n, sre.sub(m.group(3), msg, 1))
            elif s:
                return "<{}> {}".format(n, sre.sub(m.group(3), msg))
        return None

    def subswitch(self, ch, m):
        pass

    def quote_user(self, ch, m):
        pass