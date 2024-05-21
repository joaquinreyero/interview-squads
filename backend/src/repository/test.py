from sqlalchemy.exc import SQLAlchemyError

from src.config import Settings
from src.models import models


class TestRepository:

    @staticmethod
    def get_test():
        """
        The get_test function is responsible for fetching all the tests from the database.
        """
        db = Settings().configure_database()
        try:
            test = db.query(models.Test).all()
            return test
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def post_test(name: str):
        """
        The post_test function is responsible for creating a new test in the database.
        """
        db = Settings().configure_database()
        try:
            test = models.Test(name=name)
            db.add(test)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e