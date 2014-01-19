class Module:
    def __init__(self, b):
        self.bot = b
        print("Module " + self.get_name() + " loaded successfully!")
        self.active = False

    def get_hooks(self):
        return [
            ('random', self.random),
            ('choose', self.choose)
        ]

    def random(self, c, e, args):
        val = 0
        if len(args) == 1:
            # ok, choose from 0 to args
            try:
                val = random.randint(0,int(args[0]))
                c.privmsg(get_target(c, e), "I choose \x02{}\x0f!".format(val))
            except:
                c.privmsg(get_target(c, e), "\x02{}\x0f is no number!".format(args[0]))
                c.privmsg(get_target(c, e), "I choose \x02{}\x0f!".format(val))
        elif len(args) == 2:
            try:
                val = random.randint(int(args[0]),int(args[1]))
            except:
                c.privmsg(get_target(c, e), "One of \x02{}\x0f is no number!".format(args))

    def get_name(self):
        return self.__class__.__name__
