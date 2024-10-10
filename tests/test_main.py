# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app
from app.core.logging_config import logger

client = TestClient(app)


def test_process_document_with_text():
    with open("tests/comentario-economico-credito-jul2024.pdf", "rb") as file:
        response = client.post(
            "/process-document/",
            data={"message": "Por favor, resuma este documento."},
            files={
                "file": ("comentario-economico-credito-jul2024.pdf", file, "application/pdf")}
        )

    assert response.status_code == 200
    assert "summary" in response.json()


def test_process_document_without_text():
    with open("tests/comentario-economico-credito-jul2024.pdf", "rb") as file:
        response = client.post("/process-document/", files={"file": (
            "comentario-economico-credito-jul2024.pdf", file, "application/pdf")})

    assert response.status_code == 200
    assert "summary" in response.json()


def test_process_image_with_text(caplog):
    with open("tests/Captura de tela 2023-02-27 175457.png", "rb") as file:
        response = client.post("/process-image/", data={"message": "para qual sistema operacional esse erro afetou ou afeta"}, files={
                               "file": ("Captura de tela 2023-02-27 175457.png", file, "image/png")})

    assert response.status_code == 200
    assert "summary" in response.json()


def test_process_image_without_text():
    with open("tests/Captura de tela 2023-02-27 175457.png", "rb") as file:
        response = client.post(
            "/process-image/", files={"file": ("Captura de tela 2023-02-27 175457.png", file, "image/png")})

    assert response.status_code == 200
    assert "summary" in response.json()


def test_chatbot_with_image():
    response = client.post(
        "/chatbot/", data={"message": "Quando foi o ultimo titulo do Arsenal na FA cup?"})

    with open("tests/Captura de tela 2023-02-27 175457.png", "rb") as image_file:
        response = client.post(
            "/chatbot/",
            data={"message": "Quando foi o ultimo titulo do Arsenal na FA cup?"},
            files={"file": ("image.jpg", image_file, "image/jpeg")}
        )

    assert response.status_code == 200
    assert "response" in response.json()


def test_chatbot_without_image():
    response = client.post(
        "/chatbot/", data={"message": "Quando foi o ultimo titulo do Arsenal na FA cup?"})

    assert response.status_code == 200
    assert "response" in response.json()


def test_chatbot_with_pdf():
    with open("tests/comentario-economico-credito-jul2024.pdf", "rb") as file:
        response = client.post(
            "/chatbot/",
            data={"message": "Por favor, resuma este documento."},
            files={"file": ("comentario-economico-credito-jul2024.pdf", file, "application/pdf")}
        )

    assert response.status_code == 200
    assert "response" in response.json()