from sqlalchemy import Column, Integer, String, JSON
from ..database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    choices = Column(JSON)  # 선택지를 JSON으로 저장
    trait_type = Column(String)  # 이 질문이 측정하는 성향