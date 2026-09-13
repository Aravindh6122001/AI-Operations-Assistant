from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

from app.db.database import Base, engine
from app.models.user import User

app = FastAPI(title="AI Backend Platform")

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {'status': "ok"}

@app.get("/db-health")
def db_health():
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
        return {"database" : result.scalar()}