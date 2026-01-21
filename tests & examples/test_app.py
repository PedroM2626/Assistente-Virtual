import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Mock libraries
sys.modules["whisper"] = MagicMock()
sys.modules["gradio"] = MagicMock()
sys.modules["gtts"] = MagicMock()
sys.modules["torch"] = MagicMock()

# Adicionar diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import try_local_commands, process_interaction

def test_try_local_commands_wikipedia():
    with patch("webbrowser.open") as mock_open:
        result = try_local_commands("pesquisar wikipedia python")
        assert "Wikipedia" in result
        assert mock_open.called

def test_try_local_commands_youtube():
    with patch("webbrowser.open") as mock_open:
        result = try_local_commands("vídeo de música")
        assert "YouTube" in result
        assert mock_open.called

def test_try_local_commands_farmacia():
    with patch("webbrowser.open") as mock_open:
        result = try_local_commands("farmácia")
        assert "farmácias" in result
        assert mock_open.called

def test_try_local_commands_none():
    result = try_local_commands("bom dia")
    assert result is None

@patch("app.get_whisper_model")
@patch("app.text_to_speech")
def test_process_interaction_text(mock_tts, mock_whisper):
    mock_tts.return_value = "temp.mp3"
    history = []
    
    # Test text input
    new_history, text_out, audio_out = process_interaction(None, "Oi", history)
    
    assert len(new_history) == 2
    assert new_history[0]["role"] == "user"
    assert new_history[0]["content"] == "Oi"
    assert "Você disse: Oi" in new_history[1]["content"]
    assert audio_out == "temp.mp3"

@patch("app.get_whisper_model")
@patch("app.text_to_speech")
def test_process_interaction_audio(mock_tts, mock_whisper_model_func):
    mock_tts.return_value = "temp.mp3"
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"text": "Pesquisar Wikipedia Brasil"}
    mock_whisper_model_func.return_value = mock_model
    
    history = []
    
    # Test audio input
    with patch("webbrowser.open"):
        new_history, text_out, audio_out = process_interaction("audio.wav", None, history)
        
        assert len(new_history) == 2
        assert "Wikipedia" in new_history[1]["content"]
        assert audio_out == "temp.mp3"
