from fastapi import APIRouter, Form, UploadFile, File
from app.core.logging_config import logger
from app.services.pdf_processor import process_pdf 
router = APIRouter()


@router.post("/")
async def process_document_endpoint(
    message: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        contents = await file.read()
        summary = process_pdf(contents, message)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Failed to process document: {str(e)}")
        return {"error": f"Failed to process document: {str(e)}"}
