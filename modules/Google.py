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
import simplejson
from urllib import request, parse

__author__ = 'Edoxile'


class Google(Module):
    def __init__(self, b):
        super().__init__(b)
        self._base_url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&{}'

    def get_hooks(self):
        return []

    def get_commands(self):
        return [
            ('google', self.search),
            ('g', self.search)
        ]

    def search(self, c, e, args):
        url = self._base_url.format(parse.urlencode({'q': ' '.join(args)}))
        raw = request.urlopen(url)
        results = simplejson.loads(raw.read())['responseData']['results']
        if len(results) > 0:
            c.privmsg(get_target(c, e), '\x02{}\x0f - {}'.format(
                results[0]['titleNoFormatting'], results[0]['url']
            ))
        else:
            c.privmsg(get_target(c, e),
                      'Sorry {}, couldn\'nt find anything for \'{}\' on Google.'.format(e.source.nick, ' '.join(args)))
        pass