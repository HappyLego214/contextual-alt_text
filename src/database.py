from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import Depends
from typing import Annotated

sqlite_file_name = "alt-text.db"
sqlite_url = f"sqlite:///../data/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
    
SessionDep = Annotated[Session, Depends(get_session)]