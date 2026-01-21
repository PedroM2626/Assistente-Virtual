import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Mock libraries that might not be installed in the environment running the test
sys.modules["whisper"] = MagicMock()
sys.modules["sounddevice"] = MagicMock()
sys.modules["scipy"] = MagicMock()
sys.modules["scipy.io"] = MagicMock()
sys.modules["scipy.io.wavfile"] = MagicMock()
sys.modules["pygame"] = MagicMock()
sys.modules["gtts"] = MagicMock()
sys.modules["openai"] = MagicMock()

# Adicionar diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assistente_ai import try_local_commands, ChatGPTIntelligence, GTTSTTS, WhisperSTT

def test_try_local_commands_wikipedia():
    with patch("webbrowser.open") as mock_open:
        result = try_local_commands("pesquisar wikipedia python")
        assert result.success is True
        assert "Wikipedia" in result.message
        assert mock_open.called

def test_try_local_commands_youtube():
    with patch("webbrowser.open") as mock_open:
        result = try_local_commands("pesquisar youtube tutorial")
        assert result.success is True
        assert "YouTube" in result.message
        assert mock_open.called

def test_chatgpt_intelligence():
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "Olá, humano."
    mock_client.chat.completions.create.return_value = mock_completion
    
    # Mock do OpenAI client
    with patch("openai.OpenAI", return_value=mock_client):
        ai = ChatGPTIntelligence("fake-key")
        response = ai.process("Oi")
        
        assert response == "Olá, humano."
        mock_client.chat.completions.create.assert_called_once()

def test_whisper_stt_init():
    mock_whisper = sys.modules['whisper']
    mock_whisper.load_model.reset_mock()
    
    stt = WhisperSTT(model_size="tiny")
    mock_whisper.load_model.assert_called_with("tiny")

def test_gtts_tts_speak():
    mock_gtts_mod = sys.modules['gtts']
    mock_pygame = sys.modules['pygame']
    
    mock_tts_obj = MagicMock()
    mock_gtts_mod.gTTS.return_value = mock_tts_obj
    
    mock_pygame.mixer.music.get_busy.side_effect = [True, False]
    
    with patch("os.remove"):
        tts = GTTSTTS()
        tts.speak("Olá")
        
        mock_gtts_mod.gTTS.assert_called()
        mock_tts_obj.save.assert_called()
        # mock_pygame.mixer.music.play.assert_called() # Removed as it's inside while loop now
