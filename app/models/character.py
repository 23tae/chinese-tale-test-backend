from sqlalchemy import Column, Integer, String, Float, JSON
from ..database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    work = Column(String)
    description = Column(String)
    in_story = Column(String)
    traits = Column(JSON)
    image_url = Column(String)
    media_url = Column(String)
