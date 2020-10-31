import pytest

from movie.domainmodels.director import Director

def test_init():
    director1 = Director("Taika Waititi")
    assert repr(director1) == "<Director Taika Waititi>"
    director2 = Director("")
    assert director2.director_full_name is None
    director3 = Director(42)
    assert director3.director_full_name is None

def test_equal():
    director_none_1 = Director("")
    director_none_2 = Director("")
    assert director_none_1 == director_none_2
    director1 = Director("Taika Waititi")
    director2 = Director("Taika Waititi")
    assert director1 == director2
    director3 = Director("Taika Waititi1")
    director4 = Director("Taika Waititi2")
    assert director3 != director4
    assert director_none_1 != director4
    director5 = Director("Director")
    director6 = "Director"
    assert director5 != director6

def test_lt():
    director1 = Director("Director A")
    director2 = Director("Director B")
    assert director1 < director2


def test_type_mismatch():
    director = Director("Director")
    other = "Director"
    with pytest.raises(TypeError):
        return director < other


def test_hash():
    director1 = Director("Director A")
    assert hash(director1) == hash("Director A")
    director_none = Director("")
    assert hash(director_none) == hash(None)
