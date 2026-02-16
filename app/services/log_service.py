from sqlalchemy.orm import Session
from app.db.models import Log

def create_log(db: Session, agent_name: str, action: str, reward: float):
    new_log = SystemLog(
        agent_name=agent_name,
        action=action,
        reward=reward
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

def get_logs(db: Session):
    return db.query(SystemLog).all()
