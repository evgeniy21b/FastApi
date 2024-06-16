from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal, engine, Base, Task as DBTask
from models import Task as PydanticTask, TaskCreate

app = FastAPI()

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
    return db.query(DBTask).all()

@app.post("/tasks", response_model=PydanticTask)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = DBTask(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}", response_model=PydanticTask)
async def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = updated_task.title
    db_task.description = updated_task.description
    db_task.completed = updated_task.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", response_model=PydanticTask)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task

@app.get("/tasks/{task_id}", response_model=PydanticTask)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
