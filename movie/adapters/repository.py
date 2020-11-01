import abc
from typing import List, Generator

from movie.domainmodels.movie import Movie,Review,User

repo_instance: 'AbstractRepository' = None

class RepositoryException(Exception):
    def __init__(self, message=None):
        super().__init__(message)
class AbstractRepository(abc.ABC):
    @property
    @abc.abstractmethod
    def movies(self) -> Generator[Movie, None, None]:
        """" Access movies. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def users(self) -> Generator[User, None, None]:
        """" Access users. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def genres(self) -> Generator[str, None, None]:
        """" Access genre names. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def actors(self) -> Generator[str, None, None]:
        """" Access actor names. """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def directors(self) -> Generator[str, None, None]:
        """" Access director names. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie) -> None:
        """" Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title: str, year: int) -> Movie:
        """ Get a Movie from the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_id(self, movie_id: int) -> Movie:
        """ Get movie by movie id. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_n_movies(self, n: int, offset: int) -> List[Movie]:
        """ Get next n Movies from the repository starts from offset. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_total_number_of_movies(self) -> int:
        """ Get the total number of Movies in the repo. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Get the first Movie in the repo. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Get the last Movie in the repo. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_actor(self, actor: str) -> Generator[Movie, None, None]:
        """ Search the repo based on actor. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_director(self, director: str) -> Generator[Movie, None, None]:
        """ Search the repo based on director. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_genre(self, genre: str) -> Generator[Movie, None, None]:
        """ Search the repo based on genre. """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_movie(self, movie_to_delete: Movie) -> bool:
        """ Delete movie from the repo. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User) -> None:
        """ Add new user to the repo """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        """ Get existing user from the repo """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Add review """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_review(self, movie: Movie, review_id: str):
        """ remove review from movie """
        raise NotImplementedError
