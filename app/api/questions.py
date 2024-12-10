from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import question
from ..schemas.question import Question, QuestionResponse
from typing import List

router = APIRouter()

@router.get("/questions", response_model=List[Question])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(question.Question).all()

    response_questions = []
    for q in questions:
        choices_list = list(q.choices.values()) if isinstance(q.choices, dict) else q.choices
        response_questions.append(QuestionResponse(
            id=q.id,
            content=q.content,
            choices=choices_list,
            trait_type=q.trait_type
        ))

    return response_questions