from sqlalchemy import Column, String, UUID, Boolean, Integer
from ..BaseClassModel import Base 

class UserEntity(Base): 
    id = Column(UUID, primary_key=True, index=False) 
    name = Column(String) 
    email = Column(String) 
    password = Column(String) 
    verify_code = Column(Integer) 
    role = Column(Integer)
    is_verify = Column(Boolean)
