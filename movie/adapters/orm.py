from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship

from movie.domainmodels.actor import Actor
from movie.domainmodels.director import Director
from movie.domainmodels.genre import Genre
from movie.domainmodels.movie import Movie, Review, User

metadata=MetaData()


def map_model_to_tables():
    pass

