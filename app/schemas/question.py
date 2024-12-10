from pydantic import BaseModel
from typing import List, Dict

class QuestionBase(BaseModel):
    content: str
    choices: List[str]
    trait_type: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: int
    content: str
    choices: List[str]
    trait_type: str

    class Config:
        from_attributes = True