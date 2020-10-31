from itertools import islice
from typing import List, Generator, Tuple

import editdistance

from movie.adapters.repository import AbstractRepository
from movie.domainmodels.movie import Movie


def get_n_movies(n: int, offset: int, repo: AbstractRepository) -> List[Movie]:
    return repo.get_n_movies(n, offset)


def get_movie_num(repo: AbstractRepository) -> int:
    return repo.get_total_number_of_movies()


def get_n_movies_by_actor(offset: int, n: int, repo: AbstractRepository, actor: str) -> Tuple[List[Movie], int]:
    movies_gen = repo.get_movies_by_actor(actor)
    movies_count = sum(1 for _ in repo.get_movies_by_actor(actor))
    return _get_items_from_offset(offset, n, movies_gen), movies_count


def get_n_movies_by_director(offset: int, n: int, repo: AbstractRepository, director: str) -> Tuple[List[Movie], int]:
    movies_gen = repo.get_movies_by_director(director)
    movies_count = sum(1 for _ in repo.get_movies_by_director(director))
    return _get_items_from_offset(offset, n, movies_gen), movies_count


def get_n_movies_by_genre(offset: int, n: int, repo: AbstractRepository, genre: str) -> Tuple[List[Movie], int]:
    movies_gen = repo.get_movies_by_genre(genre)
    movies_count = sum(1 for _ in repo.get_movies_by_genre(genre))
    return _get_items_from_offset(offset, n, movies_gen), movies_count


def _get_items_from_offset(offset: int, n: int, gen: Generator) -> List:
    items = list(islice(gen, offset, offset + n))
    return items


def get_n_movies_by_director_fuzzy(offset: int, n: int, repo: AbstractRepository,
                                   director_fuzzy: str) -> Tuple[List[Movie], int]:
    director = _find_fuzzy_match(director_fuzzy, repo.directors)
    return get_n_movies_by_director(offset, n, repo, director)


def get_n_movies_by_actor_fuzzy(offset: int, n: int, repo: AbstractRepository,
                                actor_fuzzy: str) -> Tuple[List[Movie], int]:
    actor = _find_fuzzy_match(actor_fuzzy, repo.actors)
    return get_n_movies_by_actor(offset, n, repo, actor)


def get_n_movies_by_genre_fuzzy(offset: int, n: int, repo: AbstractRepository,
                                genre_fuzzy: str) -> Tuple[List[Movie], int]:
    genre = _find_fuzzy_match(genre_fuzzy, repo.genres)
    return get_n_movies_by_genre(offset, n, repo, genre)


def _find_fuzzy_match(fuzzy_term: str, items: Generator[str, None, None]) -> str:
    distances = ((match_item,
                  editdistance.eval(fuzzy_term.lower(), match_item.lower()))
                 for match_item in items)
    min_dist = float('inf')
    min_dist_item = None
    for item, distance in distances:
        if distance < min_dist:
            min_dist_item = item
            min_dist = distance
    return min_dist_item


def fetch_movie_info_by_id(movie_id: str, repo: AbstractRepository):
    movie_info = dict()

    movie = repo.get_movie_by_id(movie_id)
    if movie:
        movie_info['movie_title'] = movie.title
        movie_info['movie_id'] = movie_id
        movie_info['movie_description'] = movie.description
        if movie.director:
            movie_info['movie_director_full_name'] = movie.director.director_full_name
        movie_info['movie_genres'] = [g.genre_name for g in movie.genres]
        movie_info['movie_actors'] = [a.actor_full_name for a in movie.actors]
        movie_info['movie_reviews'] = [{'rating': review.rating,
                                        'comment': review.review_text,
                                        'username': review.username,
                                        'id': review.review_id}
                                       for review in movie.reviews]

    return movie_info