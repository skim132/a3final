from movie.domainmodels.person import Person


class Actor(Person):
    def __init__(self, actor_full_name: str):
        super().__init__(actor_full_name)
        self.__colleague_set =list()

    @property
    def actor_full_name(self) -> str:
        return self._name

    def add_actor_colleague(self, colleague: 'Actor'):
        if type(self) != type(colleague):
            raise TypeError(f"Expect colleague to be Actor type, instead {type(colleague)} found")
        self.__colleague_set.append(colleague)

    def check_if_this_actor_worked_with(self, colleague: 'Actor') -> bool:
        return colleague in self.__colleague_set
