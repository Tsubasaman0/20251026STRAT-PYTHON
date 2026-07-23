from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page_is_available() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "AI会議室" in response.text
    assert "作戦を入力する" in response.text
    assert "会議をはじめる" in response.text
    assert "OpenAI" in response.text
    assert "Gemini" in response.text
    assert "Claude" in response.text


def test_question_is_echoed() -> None:
    response = client.post("/api/questions", json={"question": " FastAPIとは？ "})

    assert response.status_code == 200
    assert response.json() == {"question": "FastAPIとは？"}


def test_blank_question_is_rejected() -> None:
    response = client.post("/api/questions", json={"question": "   "})

    assert response.status_code == 422
