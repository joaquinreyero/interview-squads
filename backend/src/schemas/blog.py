from pydantic import BaseModel, EmailStr, Field

class ReelLink(BaseModel):
    reel_link: str

class BlogPostDetails(BaseModel):
    title: str
    topic: str
    description: str

class CreatePost(BaseModel):
    reel_link: str
    title: str
    topic: str
    description: str
    transcription: str

class Response(BlogPostDetails):
    id : int
    reel_link: str

