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
from modules.Module import Module, get_target, Command, Hook
import sqlite3

__author__ = 'windwarrior'

table = "CREATE TABLE IF NOT EXISTS watches(" \
        "id INT PRIMARY KEY NOT NULL," \
        "watch CHAR(50) NOT NULL," \
        "watcher CHAR(50) NOT NULL," \
        ");"


class Watch(Module):
    def __init__(self, bot):
        super().__init__(bot)
        self.sqlite = sqlite3.connect('sakari.sqlite')
        self.setup_database()

    def setup_database(self):
        self.sqlite.execute(table)

    @Command('watch')
    def watch(self, c, e, args):
        msg = "Setup watches for: "
        if len(args) > 0:
            cursor = self.sqlite.cursor()
            for watch in args:
                cursor.execute('SELECT id FROM watches WHERE watch=? AND watcher=?', (watch, get_target(c, e)))
                if cursor.rowcount == 0:
                    cursor.execute('INSERT INTO watches (watch, watcher) VALUES (?,?)', (watch, get_target(c, e)))
                    msg += "{}, ".format(watch)

            cursor.close()
            c.privmsg(get_target(c, e), msg)
        else:
            c.privmsg(get_target(c, e), '{}: you need to give me names of people to watch!'.format(e.source.nick))

    @Command('watchlist')
    def watchlist(self, c, e, args):
        #Print a list of people you are watching
        pass

    @Hook('pubmsg', 'privmsg')
    def event(self, c, e):
        #Check if event originates from a watch, notify watchers, remove from db
        pass
