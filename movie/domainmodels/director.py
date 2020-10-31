from movie.domainmodels.person import Person


class Director(Person):
    @property
    def director_full_name(self) -> str:
        return self._name
