from sqlalchemy.orm import Session
from . import models, schemas

# Video CRUD operations
def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()

def get_videos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Video).offset(skip).limit(limit).all()

def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(url=video.url, title=video.title, summary=video.summary)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

# VideoComment CRUD operations
def get_video_comment(db: Session, comment_id: int):
    return db.query(models.VideoComment).filter(models.VideoComment.id == comment_id).first()

def get_video_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.VideoComment).offset(skip).limit(limit).all()

def get_video_comments_by_video(db: Session, video_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.VideoComment).filter(models.VideoComment.video_id == video_id).offset(skip).limit(limit).all()

def create_video_comment(db: Session, video_comment: schemas.VideoCommentCreate):
    db_video_comment = models.VideoComment(
        video_id=video_comment.video_id,
        comment_category=video_comment.comment_category,
        summary=video_comment.summary,
        category_count=video_comment.category_count,
        comment_insights=video_comment.comment_insights,
        representative_comments=video_comment.representative_comments
    )
    db.add(db_video_comment)
    db.commit()
    db.refresh(db_video_comment)
    return db_video_comment

def get_video_by_url(db: Session, url: str):
    return db.query(models.Video).filter(models.Video.url == url).first()

def get_comments_by_video_id(db: Session, video_id: int):
    return db.query(models.VideoComment).filter(models.VideoComment.video_id == video_id).all()
