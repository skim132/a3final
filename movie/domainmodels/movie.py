from datetime import datetime
from typing import List

from movie.domainmodels.actor import Actor
from movie.domainmodels.director import Director
from movie.domainmodels.genre import Genre

class User:
    def __init__(self, username: str, password: str):
        self._user_name = username.lower()
        self._password = password
        self._watched_movies = list()
        self._review_list = list()
        self._time_spent_watching_movies_minutes = 0

    @property
    def username(self):
        return self._user_name

    @property
    def password(self):
        return self._password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._review_list

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent_watching_movies_minutes

    def __repr__(self) -> str:
        return f"<User {self.username} {self.password}>"

    def __eq__(self, other: 'User') -> bool:
        if type(other) == User:
            return self.username == other.username
        return False

    def __lt__(self, other: 'User'):
        if type(other) == User:
            return self.username < other.username
        else:
            raise TypeError(f'Cannot compare User type with {type(other)}')

    def __hash__(self):
        return hash(self.username)

    def watch_movie(self, movie: 'Movie'):
        if movie not in self.watched_movies:
            self._watched_movies.append(movie)
            self._time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: 'Review'):
        if review not in self.reviews:
            self._review_list.append(review)

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password
        }



class Review:
    def _init_(self, movie:'Movie', user: str, review_text: str, rating: int, timestamp: float = None):
        self._movie = movie
        self._user = user
        self._review_text = review_text

        if not timestamp:
            timestamp = datetime.now().timestamp()
        self._timestamp = timestamp

        if 0 < rating < 11:
            self._rating = rating
        else:
            self._rating = None
        self._review_id = str(self._movie.id) + self._user + str(self._timestamp)

    @property
    def review_id(self) -> str:
        return self._review_id

    @property
    def movie(self) -> 'Movie':
        return self._movie

    @property
    def review_text(self) -> str:
        return self._review_text

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def username(self) -> str:
        return self._user._username

    def __repr__(self) -> str:
        movie_str = repr(self._movie) + "\n"
        review_str = f"Review: {self._review_text}.\nRating: {self._rating}"
        return movie_str + review_str

    def __eq__(self, other: 'Review') -> bool:
        res = []
        if type(other) == Review:
            for attr_k in self.__dict__.keys():
                res.append(self.__dict__[attr_k] == other.__dict__[attr_k])
            return all(res)
        return False
class Movie:
    def __init__(self, title: str, year: int,movie_id:int):
        self._id = movie_id
        self._title = None
        if isinstance(title, str) and len(title) > 0:
            self._title = title.strip()
        self._year = None
        if isinstance(year, int) and year >= 1900:
            self._year = year
        self._description = None
        self._director = None
        self._runtime_minutes = 0
        self._actors = []
        self._genres = []
        self._comments: List[Review] = list()
        self._rating = ''
        self._votes = 0
        self._revenue = 'N/A'
        self._metascore = 'N/A'
        self._voted = ''

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, ttl):
        if isinstance(ttl, str) and len(ttl) > 0:
            self._title = ttl.strip()

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self,y):
        if (y>=1900):
            self._year=y

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if isinstance(description, str) and len(description) > 0:
            self._description = description.strip()

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, director):
        if isinstance(director, Director):
            self._director = director

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime):
        if isinstance(runtime, int):
            if runtime >= 0:
                self._runtime_minutes = runtime
            else:
                raise ValueError
    @property
    def actors(self):
        return self._actors

    @actors.setter
    def actors(self, actor_list):
        self._actors = actor_list

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, genres):
        self._genres = genres

    @property
    def comments(self) -> list:
        return self._comments

    def add_comment(self, review: Review):
        self._comments.append(review)

    @property
    def rating(self):
        return round(float(self._rating), 2)

    @rating.setter
    def rating(self, rating):
        self._rating = rating

    def add_rating(self, rating: float, user: User):
        if self._voted is None:
            self._voted = ''
        if user.username not in self._voted:
            self._voted += user.username
            self._rating = str(((float(self._rating) * self._votes) + rating) / (self._votes + 1))
            self._votes += 1
            print("successes")

    @property
    def votes(self):
        return self._votes

    @votes.setter
    def votes(self, votes):
        self._votes = votes

    @property
    def revenue(self):
        return self._revenue

    @revenue.setter
    def revenue(self, revenue):
        self._revenue = revenue

    @property
    def metascore(self):
        return self._metascore

    @metascore.setter
    def metascore(self, metascore):
        self._metascore = metascore

    def __repr__(self):
        return f"<Movie {self.title}, {self.year}>"

    def __eq__(self, other: 'Movie') -> bool:
        if type(self) == type(other) and \
                self.title.lower() == other.title.lower() and \
                self.year == other.year:
            return True
        return False

    def __lt__(self, other: 'Movie') -> bool:
        if type(self) != type(other):
            raise TypeError(f"Cannot compare Movie instance with {type(other)}")
        else:
            if self.title < other.title:
                return True
            elif self.title > other.title:
                return False
            else:
                return self.year < other.year

    def __hash__(self) -> int:
        return hash((self.title, self.year))

    def add_genre(self, genre):
        if isinstance(genre, Genre):
            if genre not in self._genres:
                self._genres.append(genre)

    def remove_genre(self, genre):
        if isinstance(genre, Genre):
            if genre in self._genres:
                self._genres.remove(genre)
        elif isinstance(genre, str):
            for genre in self._genres:
                if genre.genre_name == genre:
                    self._genres.remove(genre)

    def add_actor(self, actor):
        if isinstance(actor, Actor):
            if actor not in self._actors:
                self._actors.append(actor)

    def remove_actor(self, actor):
        if isinstance(actor, Actor):
            if actor in self._actors:
                self._actors.remove(actor)
        elif isinstance(actor, str):
            for actor in self._actors:
                if actor.actor_full_name == actor:
                    self._actors.remove(actor)
