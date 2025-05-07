import os
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, engine, get_db
from . import models, schemas, crud, scheduler, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Motion API")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "change-me-in-production"),
    same_site="lax",
)

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await auth.oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await auth.oauth.google.authorize_access_token(request)
    userinfo = token["userinfo"]
    email = userinfo["email"]
    user = crud.get_user_by_email(db, email)
    if not user:
        user = crud.create_user(db, schemas.UserCreate(email=email, name=userinfo["name"], password=None))
    request.session["user"] = {"email": email}
    return RedirectResponse(url="http://localhost:5173")

@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_task = crud.create_task(db, user.id, task)
    return db_task

@app.get("/tasks", response_model=list[schemas.Task])
def list_tasks(user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_tasks(db, user.id)

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, updates: schemas.TaskUpdate, user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, updates)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if not crud.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}

@app.post("/schedule")
def run_schedule(block_size: int = 60, user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, user.id)
    scheduler.schedule_tasks(tasks, block_size)
    db.commit()
    return {"scheduled": True}

@app.get("/stats", response_model=schemas.Stats)
def stats(user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, user.id)
    return crud.compute_stats(tasks)

@app.get("/me", response_model=schemas.User)
def read_current_user(
    user: models.User = Depends(auth.get_current_user)
):
    return user