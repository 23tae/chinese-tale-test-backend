from pydantic import BaseModel
from typing import Dict

class CharacterBase(BaseModel):
    name: str
    work: str
    description: str
    image_url: str
    traits: Dict[str, float]

class CharacterCreate(CharacterBase):
    pass

class Character(CharacterBase):
    id: int

    class Config:
        from_attributes = True