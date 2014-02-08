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
from modules.Module import Module, Hook
from datetime import datetime

__author__ = 'Edoxile'


class Logger(Module):
    def __init__(self, b):
        self.formats = {
            'pubmsg': '[{}] <{}> {}',
            'pubnotice': '[{}] * <{}> {}',
            'join': '[{}] * {} joined the channel.',
            'kick': '[{}] * {} was kicked by {} ({}).',
            'mode': '[{}] * {} set mode {}.',
            'part': '[{}] * {} parted the channel ({}).',
            'quit': '[{}] * {} quit ({}).',
            'invite': '[{}] * {} invited {} into the channel.',
            'action': '[{}] * {} {}',
            'topic': '[{}] * {} set topic: {}',
            'nick': '[{}] * {} is now known as {}',
            'error': '[{}] * ERROR: {}',
        }
        super().__init__(b)

    @Hook('pubmsg', 'pubnotice', 'join', 'kick', 'mode', 'part', 'quit', 'invite', 'action', 'topic', 'nick', 'error')
    def log(self, c, e):
        print('Recieved event {}'.format(e.type))
        print('Event arguments: {}'.format(e.arguments))