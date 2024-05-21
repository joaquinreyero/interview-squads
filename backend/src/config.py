from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import logging.config
import os
from src.models.models import Base


class Settings:
    def __init__(self):
        """
        Configurate logging.
        """
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        """
        Environment variables.
        """
        self.DATABASE_URI = self.get_database_uri()
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
        self.TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")

    @staticmethod
    def get_database_uri() -> str:
        """
        DATABASE_URI_LOCAL is postgresSQL connection on Docker container running locally.
        DATABASE_URI_GCP is postgresSQL connection on Google Cloud SQL running locally.
        DATABASE_URI is postgresSQL connection on Google Cloud SQL running on GCP.
        """
        return (
                os.getenv("DATABASE_URI_LOCAL") or
                os.getenv("DATABASE_URI_GCP") or
                os.getenv("DATABASE_URI")
        )

    def configure_app(self, app: FastAPI) -> None:
        self.configure_cors(app)
        self.configure_database()

    @staticmethod
    def configure_cors(app: FastAPI) -> None:
        """
        The configure_cors function defines the origins that are allowed to access the API.
        """
        origins = ["*"]  # Allow all origins
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @staticmethod
    def configure_database():
        """
        The configure_database function is responsible for creating the database engine and session.
        """
        engine = create_engine(Settings().DATABASE_URI)
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        return session_local()

    @staticmethod
    def setup_logging():
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard'
                },
                'file': {
                    'level': 'ERROR',
                    'class': 'logging.FileHandler',
                    'filename': 'error.log',
                    'formatter': 'standard'
                },
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': True
                }
            }
        })


settings = Settings()
