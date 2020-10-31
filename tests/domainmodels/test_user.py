from movie.domainmodels.movie import User
import pytest




@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'
    for comment in user.reviews:
        # User should have an empty list of Comments after construction.
        assert False


