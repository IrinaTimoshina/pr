from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from datetime import datetime
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Middleware
@app.middleware("http")
async def db_session_middleware(request, call_next):
    response = await call_next(request)
    return response


# Upload file endpoint
@app.post("/files/", response_model=schemas.File)
async def create_file(file: UploadFile = File(...), comment: str = None, db: Session = Depends(get_db)):
    file_path = f"./uploaded_files/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_data = {
        "name": file.filename.rsplit('.', 1)[0],
        "extension": '.' + file.filename.rsplit('.', 1)[1],
        "size": os.path.getsize(file_path),
        "path": file_path,
        "created_at": datetime.utcnow(),
        "updated_at": None,
        "comment": comment
    }

    return crud.create_file(db=db, file=schemas.FileCreate(**file_data))


# List files endpoint
@app.get("/files/", response_model=list[schemas.File])
async def list_files(db: Session = Depends(get_db)):
    files = crud.get_files(db)
    return files


# Get file info endpoint
@app.get("/files/{file_name}", response_model=schemas.File)
async def get_file_info(file_name: str, db: Session = Depends(get_db)):
    file_info = crud.get_file_by_name(db, file_name)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")
    return file_info


# Delete file endpoint
@app.delete("/files/{file_name}", response_model=schemas.File)
async def delete_file(file_name: str, db: Session = Depends(get_db)):
    file_info = crud.get_file_by_name(db, file_name)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = file_info.path
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found on disk")

    crud.delete_file(db, file_info)
    return file_info


# Update file endpoint
@app.patch("/files/{file_id}", response_model=schemas.File)
async def update_file(file_id: int, file_update: schemas.FileUpdate, db: Session = Depends(get_db)):
    db_file = crud.update_file(db, file_id, file_update)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    # Update the file path and name in the file system if they have changed
    if file_update.name or file_update.path:
        new_name = file_update.name if file_update.name else db_file.name
        new_path = file_update.path if file_update.path else db_file.path
        new_extension = db_file.extension
        new_full_name = f"{new_name}{new_extension}"
        new_full_path = os.path.join(new_path, new_full_name)

        os.rename(db_file.path, new_full_path)
        db_file.path = new_full_path
        db_file.name = new_name

    return db_file
