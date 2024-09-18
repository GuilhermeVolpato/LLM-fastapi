from fastapi import APIRouter, UploadFile, File
from app.core.logging_config import logger
from app.services.pdf_processor import process_pdf  # Importar a função correta

router = APIRouter()

@router.post("/")
async def process_document_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        summary = process_pdf(contents)  # Chame a função diretamente
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Failed to process document: {str(e)}")
        return {"error": f"Failed to process document: {str(e)}"}
