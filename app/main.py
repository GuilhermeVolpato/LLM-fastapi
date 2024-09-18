from fastapi import FastAPI
from app.api.endpoints import process_document_endpoint, process_image_endpoint

app = FastAPI()

app.include_router(process_document_endpoint.router, prefix="/process-document", tags=["process_document_endpoint"])
app.include_router(process_image_endpoint.router, prefix="/process-image", tags=["process_image_endpoint"])

@app.get("/a")
def health_check():
    return 200
