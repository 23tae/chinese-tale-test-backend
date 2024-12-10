from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.ai_generator import generate_personalized_description
from typing import Dict

router = APIRouter()

@router.post("/generate-description")
async def generate_description(
    character_id: int,
    answers: Dict[int, int],
    db: Session = Depends(get_db)
):
    description = await generate_personalized_description(character_id, answers, db)
    return {"description": description}