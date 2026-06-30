from sqlalchemy.orm import Session
import models
import schemas
from auth import hash_password
from datetime import datetime


# -----------------------------
# USER CRUD
# -----------------------------

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


# -----------------------------
# TASK CRUD
# -----------------------------

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        category=task.category,
        due_date=task.due_date,
        owner_id=user_id,
        project_id=task.project_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_tasks(db: Session):
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return None

    db_task.title = task.title
    db_task.description = task.description
    db_task.priority = task.priority
    db_task.status = task.status
    db_task.category = task.category
    db_task.due_date = task.due_date
    db_task.project_id = task.project_id
    db_task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return None

    db.delete(db_task)
    db.commit()

    return {"message": "Task deleted successfully"}


# -----------------------------
# PROJECT CRUD
# -----------------------------

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(
        name=project.name,
        description=project.description
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def get_projects(db: Session):
    return db.query(models.Project).all()