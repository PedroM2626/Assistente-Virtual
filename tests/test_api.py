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


def test_api_execute_success(client):
    res = client.post("/api/execute", json={"text": "wikipedia linguagem python"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "Wikipedia" in data["message"]


def test_api_execute_unrecognized(client):
    res = client.post("/api/execute", json={"text": "foobar"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is False
    assert "Comando não reconhecido" in data["message"]