from typing import Generator, List
import csv
import os
from flask import sessions
from sqlalchemy import desc
from sqlalchemy.engine import Engine
from flask import _app_ctx_stack
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash

from movie.adapters.repository import AbstractRepository
from movie.domainmodels.actor import Actor
from movie.domainmodels.director import Director
from movie.domainmodels.genre import Genre
from movie.domainmodels.movie import User, Movie, Review
from movie.util.movie_reader import MovieFileCSVReader
actors=dict()
directors=dict()
genres=dict()

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        pass

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    @property
    def movies(self) -> Generator[Movie, None, None]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).order_by(Movie._title).all()
        except NoResultFound:
            pass
        return (movie for movie in movies)

    @property
    def users(self) -> Generator[User, None, None]:
        users = None
        try:
            users = self._session_cm.session.query(User).all()
        except NoResultFound:
            pass
        return (user for user in users)

    @property
    def genres(self) -> Generator[str, None, None]:
        genres = None
        try:
            genres = self._session_cm.session.query(Genre).all()
        except NoResultFound:
            pass
        return (genre.genre_name for genre in genres)

    @property
    def actors(self) -> Generator[str, None, None]:
        actors = None
        try:
            actors = self._session_cm.session.query(Actor).all()
        except NoResultFound:
            pass
        return (actor.actor_full_name for actor in actors)

    @property
    def directors(self) -> Generator[str, None, None]:
        directors = None
        try:
            directors = self._session_cm.session.query(Director).all()
        except NoResultFound:
            pass
        return (director.director_full_name for director in directors)

    def add_movie(self, movie: Movie) -> None:
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, title: str, year: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(
                ((Movie._title == title) & (Movie.year == year))).one()
        except NoResultFound:
            pass
        return movie

    def get_movie_by_id(self, movie_id: str) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(
                ((Movie.id == movie_id))).one()
        except NoResultFound:
            pass
        return movie

    def get_n_movies(self, n: int, offset: int) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session\
                .query(Movie)\
                .order_by(Movie._title)\
                .offset(offset)\
                .limit(n).all()
        except NoResultFound:
            pass
        return movies

    def get_total_number_of_movies(self) -> int:
        count = self._session_cm.session.query(Movie).count()
        return count

    def get_first_movie(self) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session\
                .query(Movie)\
                .order_by(Movie._title)\
                .first()
        except NoResultFound:
            pass
        return movie

    def get_last_movie(self) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session\
                .query(Movie)\
                .order_by(desc(Movie._title))\
                .first()
        except NoResultFound:
            pass
        return movie

    def get_movies_by_actor(self, actor: str) -> Generator[Movie, None, None]:
        movies = self._session_cm.session.query(Movie).filter(
            (Movie._actors).any(Actor._name == actor)
        ).order_by(Movie._title).all()
        return (i for i in movies)

    def get_movies_by_director(self, director: str) -> Generator[Movie, None, None]:
        movies = self._session_cm.session.query(Movie).filter(
            Movie._director.has(Director._name == director)
        ).order_by(Movie._title).all()
        return (i for i in movies)

    def get_movies_by_genre(self, genre: str) -> Generator[Movie, None, None]:
        movies = self._session_cm.session.query(Movie).filter(
            Movie._genres.any(Genre._genre_name == genre)
        ).order_by(Movie._title).all()
        return (i for i in movies)

    def delete_movie(self, movie_to_delete: Movie) -> bool:
        with self._session_cm as scm:
            scm.session.delete(movie_to_delete)
            scm.commit()

    def add_user(self, user: User) -> None:
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_user_name=username).one()
        except NoResultFound:
            pass
        return user

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def remove_review(self, movie: Movie, review_id: str):
        with self._session_cm as scm:
            try:
                reviews = scm.session.query(Review).filter_by(_review_id=review_id).all()
                if reviews:
                    for review in reviews:
                        scm.session.delete(review)
                scm.commit()
            except NoResultFound:
                pass
def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:

            movie_data = row
            movie_key = movie_data[0]

            # Strip any leading/trailing white space from data read.
            movie_data = [item.strip() for item in movie_data]

            movie_genres = movie_data[2].split(',')
            movie_director = movie_data[4]
            movie_actors = movie_data[5].split(',')

            # Add any new genres; associate the current movie with genres.
            for genre in movie_genres:
                if genre not in genres.keys():
                    genres[genre] = list()
                genres[genre].append(movie_key)

            if movie_director not in directors.keys():
                directors[movie_director] = list()
            directors[movie_director].append(movie_key)

            for actor in movie_actors:
                if actor.strip() not in actors.keys():
                    actors[actor.strip()] = list()
                actors[actor.strip()].append(movie_key)

            yield movie_data


def get_genre_records():
    genre_records = list()
    genre_key = 0

    for genre in genres.keys():
        genre_key = genre_key + 1
        genre_records.append((genre_key, genre))
    return genre_records

def get_director_records():
    director_records = list()
    director_key = 0

    for director in directors.keys():
        director_key = director_key + 1
        director_records.append((director_key, director))
    return director_records

def get_actor_records():
    actor_records = list()
    actor_key = 0

    for actor in actors.keys():
        actor_key = actor_key + 1
        actor_records.append((actor_key, actor))
    return actor_records

def movie_genres_generator():
    movie_genres_key = 0
    genre_key = 0

    for genre in genres.keys():
        genre_key = genre_key + 1
        for movie_key in genres[genre]:
            movie_genres_key = movie_genres_key + 1
            yield movie_genres_key, movie_key, genre_key

def movie_directors_generator():
    movie_directors_key = 0
    director_key = 0

    for director in directors.keys():
        director_key = director_key + 1
        for movie_key in directors[director]:
            movie_directors_key = movie_directors_key + 1
            yield movie_directors_key, movie_key, director_key


def movie_actors_generator():
    movie_actors_key = 0
    actor_key = 0

    for actor in actors.keys():
        actor_key = actor_key + 1
        for movie_key in actors[actor]:
            movie_actors_key = movie_actors_key + 1
            yield movie_actors_key, movie_key, actor_key


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global genres
    genres = dict()

    global directors
    directors = dict()

    global actors
    actors = dict()

    insert_genres = """
        INSERT INTO genres (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_genres, get_genre_records())

    insert_directors = """
            INSERT INTO directors (
            id, name)
            VALUES (?, ?)"""
    cursor.executemany(insert_directors, get_director_records())

    insert_actors = """
                INSERT INTO actors (
                id, name)
                VALUES (?, ?)"""
    cursor.executemany(insert_actors, get_actor_records())
    insert_movies = """
           INSERT INTO movies (
           id,title,genre,description,director,actors,movie_date,runtime,rating,votes,revenue,metascore)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'Data1000Movies.csv')))

    insert_movie_genres = """
        INSERT INTO movie_genres (
        id, movie_id, genre_id)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_genres, movie_genres_generator())

    insert_movie_directors = """
            INSERT INTO movie_directors (
            id, movie_id, director_id)
            VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_directors, movie_directors_generator())

    insert_movie_actors = """
                INSERT INTO movie_actors (
                id, movie_id, actor_id)
                VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_actors, movie_actors_generator())

    conn.commit()
    conn.close()
