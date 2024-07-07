from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)
    summary = Column(String)

    comments = relationship("VideoComment", back_populates="video")

class VideoComment(Base):
    __tablename__ = 'video_comments'

    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    comment_category = Column(String)
    summary = Column(String)
    category_count = Column(Integer)
    comment_insights = Column(String)  # Store as JSON string
    representative_comments = Column(String)  # Store as JSON string

    video = relationship("Video", back_populates="comments")