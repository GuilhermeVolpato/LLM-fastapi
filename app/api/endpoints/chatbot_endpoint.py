import base64
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import fitz
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken
from app.core.logging_config import logger
from app.services.chatbot_processor import chatBotStreamingProcessor
from app.services.pdf_processor import extract_text_by_sections

router = APIRouter()

lista_mensagem = []

@router.post("/")
async def chatBotStreaming(
    message: str = Form(...),
    file: UploadFile = File(None)
):
    try:
        image = None
        pdf = None
        if file:
            file_content = await file.read()
            print(file.content_type)
            if file.content_type == "application/pdf":
                pdf = process_pdf_file(file_content)
            elif file.content_type.startswith("image/"):
                encoded_image = base64.b64encode(file_content).decode('utf-8')
                image = encoded_image
            else:
                return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

        response = chatBotStreamingProcessor(message, lista_mensagem, image if image else None, pdf if pdf else None)
        lista_mensagem.append(response)
        return {"response": response}
    except Exception as e:
        logger.error(f"Failed to process document: {str(e)}")
        return JSONResponse(status_code=500, content={"error": f"Failed to process document: {str(e)}"})




def process_pdf_file(file_content: bytes) -> str:
    pdf_document = fitz.open(stream=file_content, filetype="pdf")
    text_sections = extract_text_by_sections(pdf_document)
    combined_text = " ".join(text_sections)

    tokenizer = tiktoken.get_encoding("cl100k_base")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=24,
        length_function=lambda text: len(tokenizer.encode(text)),
    )
    chunks = text_splitter.create_documents([combined_text])
    combined_docs = " ".join([chunk.page_content for chunk in chunks])
    
    return combined_docs