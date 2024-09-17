# tests/test_main.py
import logging
from fastapi.testclient import TestClient
from app.main import app

logger = logging.getLogger(__name__)
logging.basicConfig(filename='test.log', encoding='utf-8', level=logging.DEBUG)

client = TestClient(app)

def test_process_document():
    with open("tests/comentario-economico-credito-jul2024.pdf", "rb") as file:
        response = client.post("/process-document/", files={"file": ("comentario-economico-credito-jul2024.pdf", file, "application/pdf")})
    
    logging.info("Status Code: %d", response.status_code)
    logging.info("Response JSON: %s", response.json())

    print(response.json())
    assert response.status_code == 200
    assert "summary" in response.json()
