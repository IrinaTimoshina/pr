from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FileBase(BaseModel):
    name: str = Field(..., example="my-file")
    extension: str = Field(..., example=".txt")
    size: int = Field(..., example=10325)
    path: str = Field(..., example="/root-folder/my-storage/")
    created_at: datetime = Field(..., example="2020-05-12T13:48:10.034677")
    updated_at: Optional[datetime] = Field(None, example=None)
    comment: Optional[str] = Field(None, example="Мой первый текстовый файл")

class FileCreate(FileBase):
    pass

class FileUpdate(BaseModel):
    name: Optional[str] = Field(None, example="updated-file")
    path: Optional[str] = Field(None, example="./uploaded_files/new-path/")
    comment: Optional[str] = Field(None, example="Updated comment")

class File(FileBase):
    id: int

    class Config:
        orm_mode = True
