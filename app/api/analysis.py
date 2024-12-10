from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import matcher
from ..schemas.response import AnalysisResponse, AnswerRequest
from typing import Dict

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_answers(request: AnswerRequest, db: Session = Depends(get_db)):
    answers = {int(k): v for k, v in request.answers.items()}
    result = matcher.match_character(answers, db)
    return result