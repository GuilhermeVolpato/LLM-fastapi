# tests/test_main.py
import logging
from fastapi.testclient import TestClient
from app.main import app
from app.core.logging_config import logger

client = TestClient(app)

def test_process_document():
    with open("tests/comentario-economico-credito-jul2024.pdf", "rb") as file:
        response = client.post("/process-document/", files={"file": ("comentario-economico-credito-jul2024.pdf", file, "application/pdf")})
    
    logging.info("Status Code: %d", response.status_code)
    logging.info("Response JSON: %s", response.json())

    print(response.json())
    assert response.status_code == 200
    assert "summary" in response.json()
    
    
def test_process_image():
    with open("tests/Captura de tela 2023-02-27 175457.png", "rb") as file:
        response = client.post("/process-image/", files={"file": ("Captura de tela 2023-02-27 175457.png", file, "image/png")})
    
    logging.info("Status Code: %d", response.status_code)
    logging.info("Response JSON: %s", response.json())

    print(response.json())
    assert response.status_code == 200
    assert "summary" in response.json()
