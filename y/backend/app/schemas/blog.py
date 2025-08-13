from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BlogPostBase(BaseModel):
    title: str
    excerpt: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    is_published: bool = True

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BlogPostBase):
    pass

class BlogPost(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
