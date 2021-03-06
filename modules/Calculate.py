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
from sympy import solve, simplify

__author__ = 'Edoxile'


class Calculate(Module):
    @Command('c', 'calc', 'calculate', 'simplify')
    def simplify(self, c, e, args):
        try:
            c.privmsg(get_target(c, e), '{}: {}'.format(e.source.nick, simplify(' '.join(args))))
        except:
            c.privmsg(get_target(c, e), "Syntax error; did you mean 'solve'?")

    @Command('solve')
    def solve(self, c, e, args):
        try:
            c.privmsg(get_target(c, e), '{}: {}'.format(e.source.nick, solve(' '.join(args))))
        except:
            c.privmsg(get_target(c, e),
                      "Syntax error, please try again. Don't forget that the solver adds =0 automatically!")