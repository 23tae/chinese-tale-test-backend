from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class ResultTemplate(Base):
    __tablename__ = "result_templates"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    template_type = Column(String, nullable=False)  # 'basic', 'modern', 'advice' 등
    content = Column(String, nullable=False)
