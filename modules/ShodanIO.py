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
from exceptions import SakariException
from modules.Module import Module, get_target
from shodan import Shodan

__author__ = 'Edoxile'


class ShodanIO(Module):
    def __init__(self, b):
        super().__init__(b)
        self.key = self.bot.config.get('apikeys', 'shodan')
        if not self.key:
            raise SakariException('Couln\'t find api key for Shodan.')
        self.shodan = Shodan(self.key)

    def get_commands(self):
        return [
            ('shodan', self.query),
            ('shost', self.host)
        ]

    def get_hooks(self):
        return []

    def query(self, c, e, args):
        result = self.shodan.search(' '.join(args))
        c.privmsg(get_target(c, e), 'Found {} results.'.format(result['total']))

    def host(self, c, e, args):
        result = self.shodan.host(args[0])
        if result:
            print('{}'.format(result))
            c.privmsg(get_target(c, e),
                      'Available ports: {' + ', '.join([str(n['port']) for n in result['data']]) + '}.')
            c.privmsg(get_target(c, e), 'Services: {' + ', '.join([n['data'] for n in result['data']]) + '}.')