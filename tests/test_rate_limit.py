from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_daily_quota_blocks_after_limit(monkeypatch):
    calls = {"n": 0}

    async def fake_check_and_increment(child_id: int, limit: int):
        calls["n"] += 1
        # 1-й вызов: разрешаем, 2-й: блокируем
        if calls["n"] == 1:
            return True, 1, 1   # allowed, used, limit
        else:
            return False, 2, 1  # not allowed

    monkeypatch.setattr("app.routers.chat.check_and_increment", fake_check_and_increment, raising=True)

    payload = {"child_id": 1, "message": "Привет!"}
    r1 = client.post("/api/v1/chat/ask", json=payload)
    assert r1.status_code == 200
    assert r1.json()["blocked"] is False

    r2 = client.post("/api/v1/chat/ask", json=payload)
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["blocked"] is True
    assert "лимит" in data2["reply"].lower()



