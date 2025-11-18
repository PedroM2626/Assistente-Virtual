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


def test_homepage_loads(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Assistente Virtual" in res.data
    assert b"id=\"mic-btn\"" in res.data
    assert b"id=\"speak-toggle\"" in res.data
    assert b"id=\"audio-player\"" in res.data


def test_submit_form_executes_command(client):
    res = client.post("/", data={"text": "youtube música"})
    assert res.status_code == 200
    assert b"YouTube" in res.data