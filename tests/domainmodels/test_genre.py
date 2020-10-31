import pytest

from movie.domainmodels.genre import Genre


def test_init():
    genre1 = Genre("Horror")
    assert repr(genre1) == "<Genre Horror>"
    genre2 = Genre("")
    assert genre2.genre_name is None
    assert repr(genre2) == "<Genre None>"
    genre3 = Genre(1)
    assert genre3.genre_name is None
    assert repr(genre3) == "<Genre None>"


def test_equal():
    genre_none1 = Genre("")
    genre_none2 = Genre("")
    assert genre_none1 == genre_none2
    genre1 = Genre("Horror")
    genre2 = Genre("Horror")
    assert genre1 == genre2
    genre3 = Genre("Horror1")
    genre4 = Genre("Horror2")
    assert genre3 != genre4
    assert genre_none1 != genre4
    genre5 = Genre("Horror3")
    genre6 = "Horror3"
    assert genre5 != genre6


def test_lt():
    genre1 = Genre("Genre A")
    genre2 = Genre("Genre B")
    assert genre1 < genre2


def test_type_mismatch():
    genre = Genre("Genre")
    other = "Genre"
    with pytest.raises(TypeError):
        return genre < other


def test_hash():
    genre1 = Genre("Genre A")
    assert hash(genre1) == hash("Genre A")
    genre_none_1 = Genre("")
    assert hash(genre_none_1) == hash(None)
    genre_none_2 = Genre(0)
    assert hash(genre_none_2) == hash(None)
