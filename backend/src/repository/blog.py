from sqlalchemy.exc import SQLAlchemyError

from src.config import Settings
from src.models import models
from src.schemas.blog import CreatePost, Response

class BlogRepository:

    @staticmethod
    def post(post: CreatePost) -> int:
        db = Settings().configure_database()
        try:
            blog_post = models.BlogPost(
                link=post.reel_link,
                title=post.title,
                topic=post.topic,
                description=post.description,
                transcription=post.transcription
            )
            db.add(blog_post)
            db.commit()
            return blog_post.id
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def get(id: int) -> Response:
        db = Settings().configure_database()
        try:
            blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
            if not blog_post:
                raise Exception("Blog post not found.")
            return Response(
                id=blog_post.id,
                title=blog_post.title,
                topic=blog_post.topic,
                description=blog_post.description,
                reel_link=blog_post.link
            )
        except SQLAlchemyError as e:
            raise e