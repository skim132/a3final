import pytest

from movie.domainmodels.actor import Actor


def test_init():
    actor = Actor("Angelina Jolie")
    assert repr(actor) == "<Actor Angelina Jolie>"
    actor = Actor("")
    assert actor.actor_full_name is None
    assert repr(actor) == "<Actor None>"
    actor = Actor(42)
    assert actor.actor_full_name is None
    assert repr(actor) == "<Actor None>"


def test_equal():
    actor_none_1 = Actor("")
    actor_none_2 = Actor("")
    assert actor_none_1 == actor_none_2
    actor_1 = Actor("Angelina Jolie")
    actor_2 = Actor("Angelina Jolie")
    assert actor_1 == actor_2
    actor_1 = Actor("Angelina Jolie1")
    actor_2 = Actor("Angelina Jolie2")
    assert actor_1 != actor_2
    assert actor_none_1 != actor_1
    actor_1 = Actor("Actor")
    actor_2 = "Actor"
    assert actor_1 != actor_2


def test_lt():
    actor_1 = Actor("Actor A")
    actor_2 = Actor("Actor B")
    assert actor_1 < actor_2


def test_type_mismatch():
    actor = Actor("Actor")
    other = "Actor"
    with pytest.raises(TypeError):
        return actor < other


def test_hash():
    actor1 = Actor("Actor A")
    assert hash(actor1) == hash("Actor A")
    actor_none = Actor("")
    assert hash(actor_none) == hash(None)


def test_add_colleague():
    actor = Actor("actor")
    valid_colleague = Actor("colleague")
    invalid_colleague = "colleague"
    actor.add_actor_colleague(valid_colleague)
    assert actor.check_if_this_actor_worked_with(valid_colleague)
    with pytest.raises(TypeError):
        actor.add_actor_colleague(invalid_colleague)
