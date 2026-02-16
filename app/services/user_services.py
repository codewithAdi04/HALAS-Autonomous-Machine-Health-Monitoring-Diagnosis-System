from sqlalchemy.orm import session
from app.db import models

def create_user(db: session, username: str, email: str):
    user = models.User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: session):
    return db.query(models.User).all()

