import webbrowser
import pytest
from web_app import create_app


@pytest.fixture
def app(monkeypatch):
    def _open(url):
        return True
    monkeypatch.setattr(webbrowser, "open", _open)
    flask_app = create_app()
    flask_app.config.update({"TESTING": True})
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_tts_api_returns_wav(client):
    res = client.post("/api/tts", json={"text": "Olá mundo"})
    assert res.status_code == 200
    ct = res.headers.get("Content-Type", "")
    assert "audio/wav" in ct


def test_tts_api_empty_text(client):
    res = client.post("/api/tts", json={"text": ""})
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False