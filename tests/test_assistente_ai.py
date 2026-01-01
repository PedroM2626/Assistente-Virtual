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
    
    # Precisamos patchar openai.OpenAI dentro de assistente_ai ou onde for usado
    # Como já importamos, o modulo assistente_ai já tem o mock do sys.modules['openai']
    # Mas precisamos configurar o retorno desse mock.
    
    import assistente_ai
    assistente_ai.openai.OpenAI.return_value = mock_client
    
    ai = ChatGPTIntelligence("fake-key")
    response = ai.process("Oi")
    
    assert response == "Olá, humano."
    mock_client.chat.completions.create.assert_called_once()

def test_whisper_stt_init():
    import assistente_ai
    assistente_ai.whisper.load_model.reset_mock()
    
    stt = WhisperSTT(model_size="tiny")
    assistente_ai.whisper.load_model.assert_called_with("tiny")

def test_gtts_tts_speak():
    import assistente_ai
    
    mock_tts = MagicMock()
    assistente_ai.gTTS.return_value = mock_tts
    
    with patch("assistente_ai.os.remove"):
        tts = GTTSTTS()
        tts.speak("Olá")
        
        assistente_ai.gTTS.assert_called()
        mock_tts.save.assert_called()
        assistente_ai.pygame.mixer.music.play.assert_called()
