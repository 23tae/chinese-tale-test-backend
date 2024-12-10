from pydantic import BaseModel
from typing import Dict, Optional

class AnswerRequest(BaseModel):
    answers: Dict[str, int]

class ShareResponse(BaseModel):
    image_url: str

class CharacterInfo(BaseModel):
    id: int
    name: str
    work: str
    description: str
    image_url: str
    media_url: str

class AnalysisResponse(BaseModel):
    character: CharacterInfo
    description: str
    modern_interpretation: Optional[str] = None
    advice: Optional[str] = None
