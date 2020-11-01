from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship
from movie.domainmodels.actor import Actor
from movie.domainmodels.director import Director
from movie.domainmodels.genre import Genre
from movie.domainmodels.movie import Movie, Review, User
metadata=MetaData()
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column("time",Integer)
)
genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)
directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)
actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)
reviews= Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('comment', String(1024), nullable=False),
    Column("rating",Integer),
    Column('timestamp', DateTime, nullable=False)
)
movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('genre', String(255), nullable=True),
    Column('description', String(1024), nullable=True),
    Column('director', String(255), nullable=True),
    Column('actors', String, nullable=True),
    Column('movie_date', Integer, nullable=True),
    Column('runtime', Integer, nullable=True),
    Column('rating', String, nullable=True),
    Column('votes', Integer, nullable=True),
    Column('revenue', String, nullable=True),
    Column('metascore', String, nullable=True),
    Column('voted', String, nullable=True)
)
movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)
movie_directors = Table(
    'movie_directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('director_id', ForeignKey('directors.id'))
)
movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)

def map_model_to_tables():
    mapper(User, users, properties={
        '_User_username': users.columns.username,
        '_User_password': users.columns.password,
        '_time_spent_watching_movies_minutes':users.columns.time,
        '_review_list': relationship(Review, backref='_user')
    })
    mapper(Review, reviews, properties={
        '_review_id': reviews.columns.id,
        '_review_text': reviews.columns.comment,
        '_rating': reviews.columns.rating,
        '_timestamp': reviews.columns.timestamp
    })
    mapper(Genre, genres, properties={
        '_genre_name': genres.columns.name
    })
    mapper(Director, directors, properties={
        '_name': directors.columns.name
    })
    mapper(Actor, actors, properties={
        '_name': actors.columns.name
    })
    movies_mapper = mapper(Movie, movies, properties={
        '_Movie_id': movies.c.id,
        '_Movie_title': movies.c.title,
        '_Movie_genres': movies.c.genre,
        '_Movie_description': movies.c.description,
        '_Movie_director': movies.c.director,
        '_Movie_actors': movies.c.actors,
        '_Movie_year': movies.c.movie_date,
        '_Movie_runtime_minutes': movies.c.runtime,
        '_Movie_rating': movies.c.rating,
        '_Movie_votes': movies.c.votes,
        '_Movie_revenue': movies.c.revenue,
        '_Movie_metascore': movies.c.metascore,
        '_Movie_comments': relationship(Review, backref='_movie'),
        '_Movie_voted': movies.c.voted
    })

