import logging

from fastapi import Query, HTTPException

from src.repository.blog import BlogRepository as repository
from src.schemas.blog import CreatePost, Response
from src.utils import video_extractor
from src.utils.blog_details import generate_blog_post_details
from src.utils.channel_notification import send_channel_notification

logger = logging.getLogger(__name__)

def create(reel_link: str = Query(..., alias="reel_link")):
    try:
        transcription = video_extractor.transcribe_video_from_instagram(reel_link)
        if transcription:
            logger.debug(f"Transcription successful: {transcription}")
            blog_post_details = generate_blog_post_details(transcription)
            if not blog_post_details:
                raise HTTPException(status_code=500, detail="Failed to generate blog post details.")
            logger.debug(f"Generated blog post details: {blog_post_details}")
            create_post_data = CreatePost(
                reel_link=reel_link,
                title=blog_post_details.title,
                topic=blog_post_details.topic,
                description=blog_post_details.description,
                transcription=transcription
            )
            post_id = repository.post(create_post_data)
            response_data = Response(
                id=post_id,
                title=blog_post_details.title,
                topic=blog_post_details.topic,
                description=blog_post_details.description,
                reel_link=reel_link
            )
            send_channel_notification(response_data)
            return {
                "id": post_id,
                "transcription": transcription,
                "title": blog_post_details.title,
                "topic": blog_post_details.topic,
                "description": blog_post_details.description
            }
        else:
            logger.error("Failed to transcribe video.")
            raise HTTPException(status_code=500, detail="Failed to transcribe video.")
    except Exception as e:
        logger.error(f"Error in create function: {e}")
        raise e

def get(id: int):
    """
    Get a blog post by its ID.
    """
    try:
        return repository.get(id)
    except Exception as e:
        logger.error(f"Error in get function: {e}")
        raise HTTPException(status_code=500, detail=str(e))