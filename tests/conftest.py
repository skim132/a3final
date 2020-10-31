import os

import pytest
from movie import create_app
from movie.adapters import memory_repository
from movie.domainmodels.actor import Actor
from movie.domainmodels.director import Director
from movie.domainmodels.genre import Genre
from movie.domainmodels.movie import Movie,User

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///movie.db'
@pytest.fixture
def memory_repo():
    repo = memory_repository.MemoryRepository()
    movie_1 = Movie('Movie1', 2000,101)
    movie_2 = Movie('Movie2', 2001,102)
    movie_3 = Movie('Movie3', 2002,103)
    movie_4 = Movie('Movie4', 2003,104)
    movie_5 = Movie('Movie5', 2004,105)
    actor1 = Actor('Actor1')
    actor2 = Actor('Actor2')
    actor3 = Actor('Actor3')
    actor4 = Actor('Actor4')
    actor5 = Actor('Actor5')
    director1 = Director('Director1')
    director2 = Director('Director2')
    movie_1.add_actor(actor1)
    movie_1.add_actor(actor2)
    movie_1.add_actor(actor4)
    movie_1.add_actor(actor5)
    movie_2.add_actor(actor2)
    movie_2.add_actor(actor4)
    movie_2.add_actor(actor5)
    movie_3.add_actor(actor3)
    movie_3.add_actor(actor5)
    movie_4.add_actor(actor3)
    movie_4.add_actor(actor4)
    movie_4.add_actor(actor5)
    movie_5.add_actor(actor3)
    movie_5.add_actor(actor4)
    movie_5.add_actor(actor5)
    movie_1.director = director1
    movie_2.director = director1
    movie_3.director = director1
    movie_4.director = director2
    movie_5.director = director2
    genre1 = Genre('Genre1')
    genre2 = Genre('Genre2')
    movie_1.add_genre(genre1)
    movie_2.add_genre(genre2)
    movie_3.add_genre(genre1)
    movie_4.add_genre(genre2)
    movie_5.add_genre(genre1)
    repo.add_movie(movie_1)
    repo.add_movie(movie_2)
    repo.add_movie(movie_3)
    repo.add_movie(movie_4)
    repo.add_movie(movie_5)

    user = User(username='ExistUser', password='Password123')
    repo.add_user(user)
    return repo


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='test_user_001', password='Test123456'):
        return self._client.post(
            'auth/login',
            data={'username': username,
                  'password': password}
        )

    def logout(self):
        return self._client.get('auth/logout')

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
