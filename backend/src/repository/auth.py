from sqlalchemy.exc import SQLAlchemyError

from src.config import Settings
from src.models import models
from src.schemas import auth as schema


class AuthRepository:

    @staticmethod
    def sign_up(user: schema.SignUpInput):
        db = Settings().configure_database()
        try:
            new_user = models.Users(
                email=user.email,
                password=user.password,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return schema.User(
                id=new_user.id,
                email=new_user.email,
                password=new_user.password,
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def exist_email(email: str):
        db = Settings().configure_database()
        try:
            user = db.query(models.Users).filter(models.Users.email == email).first()
            return schema.User(
                id=user.id,
                email=user.email,
                password=user.password,
            ) if user else None
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def token_create(token: schema.TokenData):
        db = Settings().configure_database()
        try:
            new_token = models.Token(
                user_id=token.user_id,
                token=token.token,
                expiration_date=token.expiration_date,
                is_active=True
            )
            db.add(new_token)
            db.commit()
            db.refresh(new_token)
            return new_token
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def token(user_id: int):
        db = Settings().configure_database()
        try:
            token = db.query(models.Token).filter(models.Token.user_id == user_id).first()
            return schema.TokenData(
                token=token.token,
                expiration_date=token.expiration_date,
                is_active=token.is_active,
                user_id=token.user_id,
            )
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def token_exist(token: str):
        db = Settings().configure_database()
        try:
            token = db.query(models.Token).filter(models.Token.token == token).first()
            return schema.TokenData(
                token=token.token,
                expiration_date=token.expiration_date,
                is_active=token.is_active,
                user_id=token.user_id,
            ) if token else None
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def token_update(token: schema.TokenData):
        db = Settings().configure_database()
        try:
            token = db.query(models.Token).filter(models.Token.token == token.token).first()
            token.is_active = False
            db.commit()
            db.refresh(token)
            return schema.TokenData(
                token=token.token,
                expiration_date=token.expiration_date,
                is_active=token.is_active,
                user_id=token.user_id,
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def token_delate(user_id: int):
        db = Settings().configure_database()
        try:
            token = db.query(models.Token).filter(models.Token.user_id == user_id).first()
            if not token:
                raise SQLAlchemyError("Token not found.")
            db.delete(token)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
