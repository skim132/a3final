import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import NullPool
import movie.adapters.repository as repo
from movie.adapters.orm import metadata,map_model_to_tables
from movie.adapters import memory_repository,database_repository
from movie.util.constants import MOVIE_DATA_FILE,USER_DATA_FILE,REVIEW_DATA_FILE

def create_app(test_config: dict = None):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['MOVIE_DATA_PATH'] = os.path.join('movie', 'adapters', 'datafiles', MOVIE_DATA_FILE)
    app.config['USER_DATA_PATH'] = os.path.join('movie', 'adapters', 'datafiles', USER_DATA_FILE)
    app.config['REVIEW_DATA_PATH'] = os.path.join('movie', 'adapters', 'datafiles', REVIEW_DATA_FILE)

    if test_config:
        app.config.from_mapping(test_config)
        app.config['MOVIE_DATA_PATH'] = app.config['MOVIE_DATA_PATH']
        app.config['USERS_DATA_PATH'] = app.config['USERS_DATA_PATH']
        app.config['REVIEW_DATA_PATH'] = app.config['REVIEWS_DATA_PATH']

    movie_data_path = app.config['MOVIE_DATA_PATH']
    users_data_path = app.config['USER_DATA_PATH']
    reviews_data_path = app.config['REVIEW_DATA_PATH']
    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = memory_repository.MemoryRepository()
        memory_repository.populate_movies(movie_data_path, repo.repo_instance)
        memory_repository.populate_reviews(reviews_data_path,repo.repo_instance)
        memory_repository.populate_users(users_data_path,repo.repo_instance)
    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri,
                                        connect_args={"check_same_thread": False},
                                        poolclass=NullPool,
                                        echo=database_echo)
        if str(app.config['TESTING']).lower() == 'true' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE")
            clear_mappers()
            metadata.create_all(database_engine)
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            map_model_to_tables()
            database_repository.populate_movies(database_engine, movie_data_path)
            database_repository.populate_users(database_engine, users_data_path)
            database_repository.populate_reviews(database_engine, reviews_data_path)
        else:
            map_model_to_tables()

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .movie import movie
        app.register_blueprint(movie.movie_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.auth_blueprint)

        from .reviews import review
        app.register_blueprint(review.review_blueprint)

    return app
