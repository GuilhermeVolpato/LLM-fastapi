from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.core.logging_config import logger
from app.services.chatbot_processor import chatBotStreamingProcessor

router = APIRouter()

class MessageRequest(BaseModel):
    message: str
lista_mensagem = []
@router.post("/")
async def chatBotStreaming(request: MessageRequest):
    try:
        message = request.message
        print(message)
        response = chatBotStreamingProcessor(message, lista_mensagem)
        lista_mensagem.append(response)
        return {"response": response}
    except Exception as e:
        logger.error(f"Failed to process document: {str(e)}")
        return {"error": f"Failed to process document: {str(e)}"}