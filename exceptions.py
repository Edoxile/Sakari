class SakariException(Exception):
    def __init__(self, error, data=None):
        self.error = error
        self.data = data

    def __str__(self):
        return repr(self.error)
