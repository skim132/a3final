from movie.adapters.repository import AbstractRepository
from movie.domainmodels.movie import Review


def add_review(movie_id: str, username: str, comment: str, rating: int, repo: AbstractRepository) -> None:
    movie = repo.get_movie_by_id(movie_id)
    if movie:
        user = repo.get_user(username)
        review = Review(movie, user, comment, rating)
        repo.add_review(review)


def remove_review(review_id: str, movie_id: str, repo: AbstractRepository):
    movie = repo.get_movie_by_id(movie_id)
    repo.remove_review(movie, review_id)
