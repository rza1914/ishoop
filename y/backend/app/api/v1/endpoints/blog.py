from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.blog import BlogPost
from app.schemas.blog import BlogPost as BlogPostSchema, BlogPostCreate, BlogPostUpdate

router = APIRouter()

@router.get("/", response_model=List[BlogPostSchema])
def read_blog_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    posts = db.query(BlogPost).filter(BlogPost.is_published == True).offset(skip).limit(limit).all()
    return posts

@router.get("/{id}", response_model=BlogPostSchema)
def read_blog_post(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    post = db.query(BlogPost).filter(BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post

@router.post("/", response_model=BlogPostSchema)
def create_blog_post(
    *,
    db: Session = Depends(get_db),
    post_in: BlogPostCreate,
) -> Any:
    post = BlogPost(**post_in.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
