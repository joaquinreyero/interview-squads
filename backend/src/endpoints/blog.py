from fastapi import APIRouter, Query
from src.service import blog as service

router = APIRouter(
    prefix="/api/blog",
    tags=['Blog Post']
)

@router.post("/create")
def create_blog_post(reel_link: str = Query(...)):
    """
    Create a blog post based on an Instagram reel link.
    """
    return service.create(reel_link)

@router.get("/{id}")
def get_blog_post(id: int):
    """
    Get a blog post by its ID.
    """
    return service.get(id)
