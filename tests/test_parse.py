import builtins
import types
import webbrowser
import pytest
from assistente import parse_and_execute


@pytest.fixture(autouse=True)
def stub_webbrowser_open(monkeypatch):
    def _open(url):
        return True
    monkeypatch.setattr(webbrowser, "open", _open)


def test_wikipedia_command_success():
    result = parse_and_execute("wikipedia linguagem python")
    assert result.success is True
    assert "Wikipedia" in result.message


def test_youtube_command_success():
    result = parse_and_execute("youtube música clássica")
    assert result.success is True
    assert "YouTube" in result.message


def test_pharmacy_command_success():
    result = parse_and_execute("farmácia")
    assert result.success is True
    assert "farmácia" in result.message.lower()


def test_unrecognized_command():
    result = parse_and_execute("comando inexistente")
    assert result.success is False
    assert "Comando não reconhecido" in result.message