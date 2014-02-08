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
from urllib.error import HTTPError
from modules.Module import Module, get_target, Hook
import re
from urllib import request
import magic

__author__ = 'Edoxile'


class Title(Module):
    def __init__(self, b):
        super().__init__(b)
        self.re_title = re.compile('((?:https?://|www\.)[-~=\\\/a-zA-Z0-9\.:_\?&%,#\+]+)')
        self.re_html = re.compile('<title>(.+?)</title>')

    @Hook('pubmsg')
    def get_title(self, c, e):
        m = self.re_title.search(e.arguments[0])
        if m:
            try:
                url = request.urlopen(m.group(1))
            except HTTPError as ex:
                c.privmsg(get_target(c, e), 'Error: {} {}'.format(ex.code, ex.reason))
                return
            data = url.read(1024)
            info = magic.from_buffer(data).decode('utf-8')
            if 'HTML document' in info:
                t = self.re_html.search(data.decode('utf-8'))
                if t:
                    c.privmsg(get_target(c, e), '[ {} ]'.format(t.group(1)))
            else:
                c.privmsg(get_target(c, e), '[ {} ]'.format(info))
