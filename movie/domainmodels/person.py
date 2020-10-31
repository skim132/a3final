class Person:
    def __init__(self, name):
        if name == "" or type(name) is not str:
            self._name = None
        else:
            self._name = name.strip()

    def __eq__(self, other: 'Person'):
        if type(self) == type(other) and self._name == other._name:
            return True
        return False

    def __hash__(self):
        return hash(self._name)

    def __lt__(self, other: 'Person'):
        if type(self) == type(other) and self._name < other._name:
            return True
        if type(self) != type(other):
            raise TypeError(f"Cannot compare {type(self)} with {type(other)}")
        return False

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._name}>"
