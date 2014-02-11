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
from irc.client import NickMask
from modules.Module import Module, Hook, get_target
from datetime import datetime

__author__ = 'Edoxile'
from tools.Colors import IRCToHTML


class Logger(Module):
    def __init__(self, b):
        self.formats = {
            'pubmsg': '[{}] <{}> {}',
            'pubnotice': '[{}] * <{}> {}',
            'join': '[{}] * {} joined the channel',
            'kick': '[{}] * {} kicked {} ({})',
            'mode': '[{}] * {} set mode {}',
            'part': '[{}] * {} parted the channel ({})',
            'quit': '[{}] * {} quit ({})',
            'invite': '[{}] * {} sent an invitation for channel {}',
            'action': '[{}] * {} {}',
            'topic': '[{}] * {} set topic: {}',
            'nick': '[{}] * {} is now known as {}',
            'error': '[{}] * ERROR: {}',
        }
        self.to_html = IRCToHTML()
        super().__init__(b)

    @Hook('pubmsg', 'pubnotice', 'join', 'kick', 'mode', 'part', 'quit', 'invite', 'action', 'topic', 'nick', 'error')
    def log(self, c, e):
        if get_target(c, e) != e.target:
            return
        if not isinstance(e.source, NickMask):
            e.source = NickMask(e.source)
        if e.type in ['part', 'quit'] and len(e.arguments) is 0:
            data = [datetime.now().strftime('%H:%M:%S'), e.source.nick, 'Unknown reason']
        elif e.type == 'nick':
            data = [datetime.now().strftime('%H:%M:%S'), e.source.nick, e.target]
        elif e.type == 'mode':
            data = [datetime.now().strftime('%H:%M:%S'), e.source.nick, ' '.join(e.arguments)]
        else:
            data = [datetime.now().strftime('%H:%M:%S'), e.source.nick] + e.arguments
        print(self.to_html.parse('{} - {}'.format(get_target(c, e), self.formats[e.type].format(*data))))

