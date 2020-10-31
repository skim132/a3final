from datetime import date

from movie.domainmodels.movie import Movie
from movie.domainmodels.director import Director
import pytest
def test_init():
    movie = Movie("Moana", 2016,101)
    assert repr(movie) == "<Movie Moana, 2016>"
    movie = Movie("", 1899,102)
    assert movie.title is None
    assert repr(movie) == "<Movie None, None>"


def test_equal():
    movie1 = Movie("Moana", 2016,101)
    movie2 = Movie("Moana", 2016,101)
    movie3 = Movie("Moana", 2015,102)
    movie4 = Movie("Moana1", 2016,103)
    assert movie1 == movie2
    assert movie1 != movie3
    assert movie1 != movie4


def test_get_title():
    movie1 = Movie("Moana", 2016,101)
    assert movie1.title == "Moana"


def test_set_title():
    movie1 = Movie("Moana", 2016,101)
    movie1.title = "Moana1"
    assert movie1.title == "Moana1"


def test_get_year():
    movie1 = Movie("Moana", 2016,101)
    assert movie1.year == 2016


def test_set_year():
    movie1 = Movie("Moana", 2016,101)
    movie1.year = 2000
    assert movie1.year == 2000
    movie1.year = 1800
    assert movie1.year == 2000


def test_get_description():
    movie1 = Movie("Moana", 2016,101)
    assert movie1.description is None


def test_set_description():
    movie1 = Movie("Moana", 2016,101)
    movie1.description = "description"
    assert movie1.description == "description"
    movie1.description = ""
    assert movie1.description == "description"


def test_get_director():
    movie1 = Movie("Moana", 2016,101)
    assert movie1.director is None


def test_set_director():
    movie1 = Movie("Moana", 2016,101)
    director = Director("Director")
    movie1.director = director
    assert movie1.director == director
    director_invalid = "Director"
    movie1.director = director_invalid
    assert movie1.director == director


def test_get_runtime_minutes():
    movie1 = Movie("Moana", 2016,101)
    movie1.runtime_minutes = 100
    assert movie1.runtime_minutes == 100

