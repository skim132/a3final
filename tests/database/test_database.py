from movie.adapters.database_repository import SqlAlchemyRepository
from movie.domainmodels.movie import User, Movie, Review

def test_repository_can_retrieve_article_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_movies = repo.get_total_number_of_movies()
    assert number_of_movies == 1000
def test_repository_can_retrieve_movies_by_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = list(repo.get_movies_by_actor('Vin Diesel'))
    assert len(movies) == 1
    movie = repo.get_movie('Guardians of the Galaxy', 2014)
    assert movie in movies