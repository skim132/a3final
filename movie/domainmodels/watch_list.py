from movie.domainmodels.movie import Movie
class WatchList:
    def __init__(self):
        self._watched_movies = list()

    def add_movie(self, movie: Movie):
        if movie not in self._watched_movies:
            self._watched_movies.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self._watched_movies:
            self._watched_movies.remove(movie)

    def select_movie_to_watch(self, index):
        try:
            return self._watched_movies[index]
        except IndexError:
            return None

    def size(self):
        return len(self._watched_movies)

    def first_movie_in_watchlist(self):
        if len(self._watched_movies) > 0:
            return self._watched_movies[0]
        return None

    def __iter__(self):
        return iter(self._watched_movies)

    def __next__(self):
        return next(self._watched_movies)
