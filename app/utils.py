from fastapi import Request
from app.database import SessionLocal

def get_db(request: Request):
    return request.state.db
