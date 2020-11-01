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
    app.config['MOVIE_DATA_PATH'] = os.path.join('C:',os.sep,'a3final','movie', 'adapters', 'datafiles',MOVIE_DATA_FILE)
    app.config['USER_DATA_PATH'] = os.path.join('C:',os.sep,'a3final','movie', 'adapters', 'datafiles',USER_DATA_FILE)
    app.config['REVIEW_DATA_PATH'] = os.path.join('C:',os.sep,'a3final','movie', 'adapters', 'datafiles',REVIEW_DATA_FILE)
    app.config['DATA_PATH'] = os.path.join('C:', os.sep, 'a3final', 'movie', 'adapters', 'datafiles')
    if test_config:
        app.config.from_mapping(test_config)
        app.config['MOVIE_DATA_PATH'] = app.config['MOVIE_DATA_PATH']
        app.config['USERS_DATA_PATH'] = app.config['USERS_DATA_PATH']
        app.config['REVIEW_DATA_PATH'] = app.config['REVIEWS_DATA_PATH']

    movie_data_path = app.config['MOVIE_DATA_PATH']
    users_data_path = app.config['USER_DATA_PATH']
    reviews_data_path = app.config['REVIEW_DATA_PATH']
    data_path=app.config['DATA_PATH']
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
        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()
            database_repository.populate(database_engine, data_path)
        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()
            # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
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

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app
