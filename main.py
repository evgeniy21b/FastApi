from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine, Base, Task as DBTask
from models import Task as PydanticTask, TaskCreate

import logging

app = FastAPI()

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание базы данных при запуске
Base.metadata.create_all(bind=engine)

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks", response_model=List[PydanticTask])
async def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(DBTask).all()
    logger.info("Retrieved tasks: %s", tasks)
    return tasks

@app.post("/tasks", response_model=PydanticTask)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    logger.info("Creating task with title: %s", task.title)
    db_task = DBTask(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    try:
        db.commit()
        db.refresh(db_task)
        logger.info("Task created: %s", db_task)
    except Exception as e:
        db.rollback()
        logger.error("Error creating task: %s", str(e))
        raise HTTPException(status_code=400, detail="Error creating task")
    return db_task

@app.put("/tasks/{task_id}", response_model=PydanticTask)
async def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    logger.info("Updating task with id: %d", task_id)
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        logger.error("Task not found: %d", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = updated_task.title
    db_task.description = updated_task.description
    db_task.completed = updated_task.completed
    try:
        db.commit()
        db.refresh(db_task)
        logger.info("Task updated: %s", db_task)
    except Exception as e:
        db.rollback()
        logger.error("Error updating task: %s", str(e))
        raise HTTPException(status_code=400, detail="Error updating task")
    return db_task

@app.delete("/tasks/{task_id}", response_model=PydanticTask)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    logger.info("Deleting task with id: %d", task_id)
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        logger.error("Task not found: %d", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        db.delete(db_task)
        db.commit()
        logger.info("Task deleted: %s", db_task)
    except Exception as e:
        db.rollback()
        logger.error("Error deleting task: %s", str(e))
        raise HTTPException(status_code=400, detail="Error deleting task")
    return db_task

@app.get("/tasks/{task_id}", response_model=PydanticTask)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    logger.info("Retrieving task with id: %d", task_id)
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        logger.error("Task not found: %d", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info("Task retrieved: %s", db_task)
    return db_task
