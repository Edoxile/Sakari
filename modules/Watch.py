from modules.Module import Module, get_target
import sqlite3

__author__ = 'Lennart'

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

    def get_commands(self):
        return [
            ('watch', self.watch)
        ]

    def get_hooks(self):
        return []

    def watch(self, c, e, args):
        msg = "Setup watches for: "
        if len(args) > 0:
            cursor = self.sqlite.cursor()
            for watch in args:
                cursor.execute("SELECT id FROM watches WHERE watch=? AND watcher=?", (watch, get_target(c, e)))
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO watches (watch, watcher) VALUES (?,?)", (watch, get_target(c, e)))
                    msg += "{}, ".format(watch)

            cursor.close()
            c.privmsg(get_target(c, e), msg)
        else:
            c.privmsg(get_target(c, e), "you need to give me names")


