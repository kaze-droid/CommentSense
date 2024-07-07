from pydantic import BaseModel, EmailStr
from typing import List, Optional

class VideoCommentBase(BaseModel):
    video_id: int
    comment_category: Optional[str] = None
    summary: Optional[str] = None
    category_count: Optional[int] = None
    comment_insights: Optional[str] = None  # JSON string
    representative_comments: Optional[str] = None  # JSON string

class VideoCommentCreate(VideoCommentBase):
    pass

class VideoComment(VideoCommentBase):
    id: int
    video_id: int

    class Config:
        orm_mode: True

class VideoBase(BaseModel):
    url: str
    title: Optional[str] = None
    summary: Optional[str] = None

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: int
    comments: List[VideoComment] = []

    class Config:
        orm_mode: True
