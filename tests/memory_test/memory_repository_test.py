import pytest
from movie.domainmodels.actor import Actor
from movie.domainmodels.director import Director
from movie.domainmodels.genre import Genre
from movie.domainmodels.movie import Movie,User
def test_repository_can_add_movie(memory_repo):
    movie = Movie('Test Movie', 2020,139)
    memory_repo.add_movie(movie)
    assert memory_repo.get_movie('test movie', 2020) is movie
    assert memory_repo.get_total_number_of_movies() == 6


def test_repository_can_get_movie(memory_repo):
    movie = Movie('Test Movie', 2020,139)
    memory_repo.add_movie(movie)
    assert memory_repo.get_movie('test movie', 2020) is movie


def test_repository_can_not_get_movie(memory_repo):
    assert memory_repo.get_movie('Not Existing Movie', 9999) is None


def test_repository_get_first_movie(memory_repo):
    movie_1 = Movie("Movie1", 2000,111)
    assert memory_repo.get_first_movie() == movie_1


def test_repository_get_last_movie(memory_repo):
    movie_5 = Movie("Movie5", 2004,114)
    assert memory_repo.get_last_movie() == movie_5


def test_repository_get_n_movies(memory_repo):
    movie_1 = Movie("Movie1", 2000,111)
    movie_2 = Movie("Movie2", 2001,112)
    movies = memory_repo.get_n_movies(2, 0)
    assert len(movies) == 2
    assert movie_1 in movies
    assert movie_2 in movies


def test_repository_get_more_than_n_movies(memory_repo):
    movies = memory_repo.get_n_movies(10, 0)
    assert len(movies) == 5


def test_repository_get_n_movies_with_offset(memory_repo):
    movie_3 = Movie("Movie3", 2002,114)
    movie_4 = Movie("Movie4", 2003,115)
    movies = memory_repo.get_n_movies(2, 2)
    assert len(movies) == 2
    assert movie_3 in movies
    assert movie_4 in movies


def test_get_total_numer_of_movies(memory_repo):
    assert memory_repo.get_total_number_of_movies() == 5


def test_delete_movie(memory_repo):
    movie_3 = Movie("Movie3", 2002,112)
    res = memory_repo.delete_movie(movie_3)
    assert res is True
    assert memory_repo.get_total_number_of_movies() == 4




def test_get_movie_by_id(memory_repo):
    movie = Movie('Test Movie', 2020,101)
    memory_repo.add_movie(movie)
    movie_id = movie.id
    assert memory_repo.get_movie_by_id(movie_id) is movie


def test_get_movie_by_actor(memory_repo):
    movie = Movie('Test Movie', 2020,102)
    movie.add_actor(Actor('Actor1'))
    movie.add_actor(Actor('Actor2'))
    memory_repo.add_movie(movie)
    assert movie in memory_repo.get_movies_by_actor('Actor1')
    assert movie in memory_repo.get_movies_by_actor('Actor2')


def test_get_movie_by_director(memory_repo):
    movie = Movie('Test Movie', 2020,202)
    movie.director = Director('Director1')
    memory_repo.add_movie(movie)
    assert movie in memory_repo.get_movies_by_director('Director1')


def test_get_movie_by_genre(memory_repo):
    movie = Movie('Test Movie', 2020,202)
    movie.add_genre(Genre('Genre1'))
    movie.add_genre(Genre('Genre2'))
    memory_repo.add_movie(movie)
    assert movie in memory_repo.get_movies_by_genre('Genre1')
    assert movie in memory_repo.get_movies_by_genre('Genre2')


def test_add_user(memory_repo):
    user = User('TestUser', 'Test123456')
    memory_repo.add_user(user)
    assert user is memory_repo.get_user('TestUser')
