from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

# database setup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# models
class RunDB(Base):
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    distance = Column(Float, nullable=False)
    weather = Column(JSON, nullable=False)
    clothing = Column(JSON, nullable=False)
    comfort = Column(Integer, nullable=False)

# pydantic models
class RunBase(BaseModel):
    date: datetime
    distance: float 
    weather: dict 
    clothing: Optional[dict] = None
    comfort: Optional[int] = None

class RunCreate(RunBase):
    pass

class Run(RunBase):
    id: int
    
    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/runs", response_model=List[Run])
def get_runs(db: Session = Depends(get_db)):
    runs = db.query(RunDB).all()
    return runs

@app.post("/api/runs", response_model=Run)
def create_run(run: RunCreate, db: Session = Depends(get_db)):
    db_run = RunDB(**run.dict())
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

@app.post("/api/recommend")
def recommend_clothing():
    # placeholder
    return {"recommendation": "t-shirt and shorts"}

# create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    