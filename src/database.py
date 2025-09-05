from sqlalchemy import create_engine 
from .models.BaseClassModel import Base

sqlite_database = "sqlite://vsdifficult.db" 

engine = create_engine(sqlite_database) 
Base.metadata.create_all(bind=engine)
