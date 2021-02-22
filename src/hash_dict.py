__all__ = ['HashableDict']

class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
