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
import hashlib
from modules.Module import Module, get_target
import sqlite3

__author__ = 'Edoxile'


class Auth(Module):
    def __init__(self, b):
        super().__init__(b)
        self.sqlite = sqlite3.connect('sakari.sqlite')
        # User 'objects' consist of a dict with {nick: (username, ip, level)}
        self.users = {}

    def get_hooks(self):
        return [
            ('login', self.login),
            ('logout', self.logout),
            ('whoami', self.whoami),
            ('whois', self.whois)
        ]

    def login(self, c, e, args):
        if e.source.nick in self.users.keys():
            c.privmsg(get_target(c, e), "Already logged in as %s." % self.users[e.source.nick][1])
        else:
            args[1] = hashlib.sha512(args[1].encode('utf-8')).hexdigest()
            cursor = self.sqlite.cursor()
            cursor.execute("SELECT level FROM users WHERE username=? AND password=?", (args[0], args[1]))
            level = cursor.fetchone()
            if level is not None:
                self.users.update({e.source.nick: (args[0], e.source, int(level))})
                c.privmsg("Logged in successfully!")
            else:
                c.privmsg("The username/password combination is not known.")

    def logout(self, c, e, args):
        if e.source.nick in self.users.keys():
            del self.users[e.source.nick]
            c.privmsg(get_target(c, e), "Successfully logged out!")
        else:
            c.privmsg(get_target(c, e), "Can't log out if you aren't logged in...")

    def whoami(self, c, e, args):
        if e.source.nick in self.users.keys():
            c.privmsg(get_target(c, e), "You're not logged in at the moment")
        else:
            data = self.users[e.source.nick]
            c.privmsg(get_target(c, e),
                      "You're logged in as \x02{}\x0f with access level \x02{}\x0f.".format(data[0], data[2]))

    def whois(self, c, e, args):
        if args[0] in self.users.keys():
            data = self.users[e.source.nick]
            c.privmsg(get_target(c, e),
                      "You're logged in as \x02{}\x0f with access level \x02{}\x0f.".format(data[0], data[2]))
        else:
            c.privmsg(get_target(c, e), "{} is not logged in at the moment.".format(args[0]))

    def get_level(self, c, e):
        if e.source.nick in self.users.keys():
            if self.users[e.source.nick][1] == e.source:
                return self.users[e.source.nick][2]
            else:
                del self.users[e.source.nick]
                c.privmsg(get_target(c, e), "Your host changed after logging in. You have to log in again.")
                return 0