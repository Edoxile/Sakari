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
import subprocess

__author__ = 'Edoxile'


class Python(Module):
    def get_commands(self):
        return [
            ('py', self.run)
        ]

    def get_hooks(self):
        return []

    def run(self, c, e, args):
        cmd = ' '.join(args).split(';')[0]
        try:
            c.privmsg(get_target(c, e),
                      subprocess.check_output(['python', '-c', 'print({})'.format(cmd)]).decode('utf-8').replace('\n',
                                                                                                                 ''))
        except subprocess.CalledProcessError as ex:
            c.privmsg(get_target(c, e),
                      'Exception running python code: {}'.format(ex.output.encode('utf-8').replace('\n', ' ')))