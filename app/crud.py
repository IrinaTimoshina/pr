from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def create_file(db: Session, file: schemas.FileCreate):
    db_file = models.File(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_files(db: Session):
    return db.query(models.File).all()


def get_file_by_name(db: Session, file_name: str):
    return db.query(models.File).filter(models.File.name == file_name).first()


def delete_file(db: Session, file: models.File):
    db.delete(file)
    db.commit()


def update_file(db: Session, file_id: int, file_update: schemas.FileUpdate):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if not db_file:
        return None

    if file_update.name:
        db_file.name = file_update.name
    if file_update.path:
        db_file.path = file_update.path
    if file_update.comment:
        db_file.comment = file_update.comment

    db_file.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_file)
    return db_file
