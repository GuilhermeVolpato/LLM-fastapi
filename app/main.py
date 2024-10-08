from fastapi import FastAPI
from app.api.endpoints import process_document_endpoint, process_image_endpoint, chatbot_endpoint

app = FastAPI()

app.include_router(process_document_endpoint.router, prefix="/process-document", tags=["process_document_endpoint"])
app.include_router(process_image_endpoint.router, prefix="/process-image", tags=["process_image_endpoint"])
app.include_router(chatbot_endpoint.router, prefix="/chatbot", tags=["chatbot_endpoint"])

@app.get("/")
def health_check():
    return 200
