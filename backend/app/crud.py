from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional

from . import models, schemas

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(email=user.email, name=user.name, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tasks(db: Session, user_id: int) -> List[models.Task]:
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def create_task(db: Session, user_id: int, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, updates: schemas.TaskUpdate) -> Optional[models.Task]:
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None
    for k, v in updates.dict(exclude_unset=True).items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True

def compute_stats(tasks: List[models.Task]) -> schemas.Stats:
    if not tasks:
        return schemas.Stats(completion_rate=0, missed_tasks=0, streak=0)
    completed = [t for t in tasks if t.completed]
    completion_rate = len(completed) / len(tasks)
    today = datetime.utcnow().date()
    streak = 0
    for i in range(30):
        day = today - timedelta(days=i)
        day_tasks = [t for t in completed if t.scheduled_start and t.scheduled_start.date() == day]
        if day_tasks:
            streak += 1
        else:
            break
    missed = [t for t in tasks if not t.completed and t.scheduled_end and t.scheduled_end < datetime.utcnow()]
    return schemas.Stats(completion_rate=completion_rate, missed_tasks=len(missed), streak=streak)
