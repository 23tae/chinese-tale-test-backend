from fastapi import APIRouter, HTTPException
from ..services.image_gen import generate_share_image

router = APIRouter()

@router.post("/generate-share-image")
async def create_share_image(character_id: int, result_text: str):
    try:
        image_url = await generate_share_image(character_id, result_text)
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))