from fastapi import FastAPI
from .sql_app import models
from .sql_app.database import SessionLocal, engine

def create_app():
    app=FastAPI()
    app.state.my_state=False

    return app

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

app=create_app()