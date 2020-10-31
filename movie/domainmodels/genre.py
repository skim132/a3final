class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self) -> str:
        return f"<Genre {self.genre_name}>"

    def __eq__(self, other: 'Genre') -> bool:
        if type(self) == type(other) and self.genre_name == other.genre_name:
            return True
        return False

    def __lt__(self, other: 'Genre') -> bool:
        if type(self) == type(other) and self.genre_name < other.genre_name:
            return True
        if type(self) != type(other):
            raise TypeError(f"Cannot compare Genre instance with {type(other)}")
        return False

    def __hash__(self):
        return hash(self.genre_name)
