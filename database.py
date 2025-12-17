from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
import os
from dotenv import load_dotenv

load_dotenv()  

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL:", os.getenv("DATABASE_URL"))

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL Environment variable is not set")

engine = create_engine(DATABASE_URL, echo=True)

engine.connect()
print("Connected!")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session




SessionDep = Annotated[Session, Depends(get_session)]