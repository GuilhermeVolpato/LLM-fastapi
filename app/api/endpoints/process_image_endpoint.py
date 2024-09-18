from fastapi import APIRouter, UploadFile, File
from app.core.logging_config import logger
from app.services.image_processor import process_image_from_bytes

router = APIRouter()

@router.post("/")
async def process_image_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        summary = process_image_from_bytes(contents)  # Chame a função corretamente
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Failed to process image: {str(e)}")
        return {"error": f"Failed to process image: {str(e)}"}
