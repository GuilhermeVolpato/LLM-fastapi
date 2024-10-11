import base64
from fastapi import APIRouter, Form, UploadFile, File
from app.core.logging_config import logger
from app.services.image_processor import process_image_from_bytes

router = APIRouter()


@router.post("/")
async def process_image_endpoint(
    message: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        contents = await file.read()
        encoded_image = base64.b64encode(contents).decode('utf-8')

        summary = process_image_from_bytes(
            encoded_image, message)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Failed to process image: {str(e)}")
        return {"error": f"Failed to process image: {str(e)}"}
