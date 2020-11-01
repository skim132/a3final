import csv
import shutil
import tempfile
from bisect import insort_left
from typing import List, Generator

from flask import has_app_context, current_app

from movie.adapters.repository import AbstractRepository
from movie.domainmodels.movie import Movie, Review, User
from movie.util.movie_reader import MovieFileCSVReader
from movie.util.review_reader import ReviewFileCSVReader
from movie.util.user_reader import UserFileCSVReader


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._actors_index = dict()
        self._directors_index = dict()
        self._genres_index = dict()

        self._users = list()

    @property
    def movies(self) -> Generator[Movie, None, None]:
        return (movie for movie in self._movies)

    @property
    def users(self) -> Generator[User, None, None]:
        return (user for user in self._users)

    @property
    def genres(self) -> Generator[str, None, None]:
        return (genre for genre in self._genres_index)

    @property
    def actors(self) -> Generator[str, None, None]:
        return (actor for actor in self._actors_index)

    @property
    def directors(self) -> Generator[str, None, None]:
        return (direcotr for direcotr in self._directors_index)

    def add_movie(self, movie: Movie) -> bool:
        if movie in self._movies:
            return False
        insort_left(self._movies, movie)

        self._update_movie_index(movie)
        self._update_actor_index(movie)
        self._update_director_index(movie)
        self._update_genre_index(movie)
        return True

    def _update_movie_index(self, movie: Movie):
        self._movies_index[movie.id] = movie

    def _update_actor_index(self, movie: Movie):
        if movie.actors:
            for actor in movie.actors:
                movie_ids = self._actors_index.get(actor.actor_full_name, [])
                movie_ids.append(movie.id)
                self._actors_index.update({
                    actor.actor_full_name: movie_ids
                })

    def _update_director_index(self, movie: Movie):
        if movie.director:
            movie_ids = self._directors_index.get(movie.director.director_full_name, [])
            movie_ids.append(movie.id)
            self._directors_index.update({
                movie.director.director_full_name: movie_ids
            })

    def _update_genre_index(self, movie: Movie):
        if movie.genres:
            for genre in movie.genres:
                movie_ids = self._genres_index.get(genre.genre_name, [])
                movie_ids.append(movie.id)
                self._genres_index.update({
                    genre.genre_name: movie_ids
                })

    def get_movie(self, title: str, year: int) -> Movie:
        return next((movie for movie in self._movies
                     if movie.title.lower() == title.lower()
                     and movie.year == year),
                    None)

    def get_movie_by_id(self, movie_id: int) -> Movie:
        return self._movies_index.get(movie_id)

    def get_n_movies(self, n: int, offset: int = 0) -> List[Movie]:
        return self._movies[offset: offset + n]

    def get_total_number_of_movies(self) -> int:
        return len(self._movies)

    def get_first_movie(self) -> Movie:
        return self._get_movies_by_idx(0)

    def get_last_movie(self) -> Movie:
        return self._get_movies_by_idx(-1)

    def _get_movies_by_idx(self, idx: int) -> Movie:
        try:
            movie = self._movies[idx]
        except IndexError:
            movie = None
        return movie

    def get_movies_by_actor(self, actor: str) -> Generator[Movie, None, None]:
        return self._get_movies_from_index(self._actors_index, actor)

    def get_movies_by_director(self, director: str) -> Generator[Movie, None, None]:
        return self._get_movies_from_index(self._directors_index, director)

    def get_movies_by_genre(self, genre: str) -> Generator[Movie, None, None]:
        return self._get_movies_from_index(self._genres_index, genre)

    def _get_movies_from_index(self, index: dict, lookup_key: str):
        movies_ids = index.get(lookup_key, [])
        return (self.get_movie_by_id(movie_id) for movie_id in movies_ids)

    def delete_movie(self, movie_to_delete: Movie) -> bool:
        if movie_to_delete in self._movies:
            self._movies.remove(movie_to_delete)
            return True
        return False

    def add_user(self, user: User) -> None:
        if user not in self._users:
            self._users.append(user)
        if has_app_context():
            self._save_users_to_disk(current_app.config['USER_DATA_PATH'])

    def _save_users_to_disk(self, data_path: str) -> None:
        with open(data_path, 'w', newline='') as f:
            user_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for user in self._users:
                user_writer.writerow([user.username, user.password])

    def add_user_to_memory(self, user: User) -> None:
        if user not in self._users:
            self._users.append(user)

    def get_user(self, username: str) -> User:
        return next((user for user in self._users
                     if user.username.strip().lower() == username.strip().lower()),
                    None)

    def add_review(self, review: Review):
        review.movie.add_review(review)
        if has_app_context():
            self._save_reviews_to_disk(current_app.config['REVIEW_DATA_PATH'], review)

    def remove_review(self, movie: Movie, review_id: str):
        movie.remove_review_by_id(review_id)
        if has_app_context():
            self._remove_review_from_disk(current_app.config['REVIEW_DATA_PATH'], review_id)

    @staticmethod
    def _save_reviews_to_disk(data_path: str, review: Review) -> None:
        with open(data_path, 'a', newline='') as f:
            review_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            review_writer.writerow([review.review_id, review.movie.id,
                                    review.username, review.rating,
                                    review.review_text, review.timestamp])

    @staticmethod
    def _remove_review_from_disk(data_path: str, review_id: str) -> None:
        tmp_out = tempfile.NamedTemporaryFile(mode='w', newline='', delete=False)
        with open(data_path, 'r', newline='') as input, tmp_out:
            input_reviews = csv.reader(input, delimiter=',')
            writer = csv.writer(tmp_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for review in input_reviews:
                if review[0] != review_id:
                    writer.writerow(review)
        shutil.move(tmp_out.name, data_path)


def populate_movies(data_path: str, repo: MemoryRepository) -> None:
    reader = MovieFileCSVReader(data_path)
    reader.read_csv_file()
    for movie in reader.dataset_of_movies:
        repo.add_movie(movie)


def populate_users(data_path: str, repo: MemoryRepository) -> None:
    reader = UserFileCSVReader(data_path)
    for user in reader.dataset_of_users:
        repo.add_user_to_memory(user)


def populate_reviews(data_path: str, repo: MemoryRepository) -> None:
    reader = ReviewFileCSVReader(data_path)
    for review_fields in reader.dataset_of_reviews:
        movie_id = review_fields.get('movie_id')
        user_name = review_fields.get('username')
        rating = review_fields.get('rating')
        comment = review_fields.get('comment')
        timestamp = review_fields.get('timestamp')
        movie = repo.get_movie_by_id(movie_id)
        user = repo.get_user(user_name)
        review = Review(movie, user, comment, rating, timestamp)
        movie.add_review(review)
