import csv
from typing import List

from movie.domainmodels.actor import Actor
from movie.domainmodels.director import Director
from movie.domainmodels.genre import Genre
from movie.domainmodels.movie import Movie


class MovieFileCSVReader(object):
    def __init__(self, data_path):
        self._data_path = data_path
        self._dataset_of_movies = set()
        self._dataset_of_actors = set()
        self._dataset_of_directors = set()
        self._dataset_of_genres = set()

    @property
    def dataset_of_movies(self) -> List[Movie]:
        return list(self._dataset_of_movies)

    @property
    def dataset_of_actors(self) -> List[Actor]:
        return list(self._dataset_of_actors)

    @property
    def dataset_of_directors(self) -> List[Director]:
        return list(self._dataset_of_directors)

    @property
    def dataset_of_genres(self) -> List[Genre]:
        return list(self._dataset_of_genres)

    def _read_field(self, record: dict, key: str, sep: str) -> List[str]:
        str_objects = record.get(key)
        if str_objects:
            return str_objects.split(sep)
        return []

    def read_csv_file(self):
        with open(self._data_path, mode='r', encoding='utf-8-sig') as f:
            records = csv.DictReader(f)
            for record in records:
                movie = Movie(record.get('Title'), int(record.get('Year', 0)))

                for actor in self._read_field(record, 'Actors', ','):
                    actor = Actor(actor)
                    movie.add_actor(actor)
                    self._dataset_of_actors.add(actor)

                for genre in self._read_field(record, 'Genre', ','):
                    genre = Genre(genre)
                    movie.add_genre(genre)
                    self._dataset_of_genres.add(genre)

                for director in self._read_field(record, 'Director', ','):
                    director = Director(director)
                    movie.set_director(director)
                    self._dataset_of_directors.add(director)

                movie.description = record.get('Description')
                movie.runtime_minutes = int(record.get('Runtime (Minutes)'))

                self._dataset_of_movies.add(movie)
