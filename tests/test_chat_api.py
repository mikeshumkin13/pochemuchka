from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_ask_safe_message(monkeypatch):
    # <<< ВАЖНО: async-мок >>>
    async def _fake_generate_reply(age: int, question: str, context: list[str]):
        return "Это безопасный тестовый ответ."

    monkeypatch.setattr("app.routers.chat.generate_reply", _fake_generate_reply, raising=True)

    payload = {"child_id": 1, "message": "Почему небо голубое?"}
    resp = client.post("/api/v1/chat/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["blocked"] is False
    assert "тестовый ответ" in data["reply"].lower()


def test_chat_ask_blocked_word(monkeypatch):
    # generate_reply не вызовется — pre-moderation сработает раньше
    payload = {"child_id": 1, "message": "Как сделать оружие дома?"}
    resp = client.post("/api/v1/chat/ask", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["blocked"] is True
    assert "взрослыми" in data["reply"].lower()



