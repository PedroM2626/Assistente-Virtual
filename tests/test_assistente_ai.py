import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Adicionar diretório pai ao path para importar assistente_ai
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assistente_ai import try_local_commands, ActionResult, ChatGPTIntelligence, GTTSTTS

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

def test_try_local_commands_none():
    result = try_local_commands("ola mundo")
    assert result is None

def test_chatgpt_intelligence():
    with patch("openai.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Olá, humano."
        mock_client.chat.completions.create.return_value = mock_completion
        
        ai = ChatGPTIntelligence("fake-key")
        response = ai.process("Oi")
        
        assert response == "Olá, humano."
        mock_client.chat.completions.create.assert_called_once()

def test_gtts_tts():
    # Testar se gTTS é chamado corretamente e pygame tenta tocar
    with patch("assistente_ai.gTTS") as mock_gtts, \
         patch("assistente_ai.pygame.mixer") as mock_mixer, \
         patch("assistente_ai.os.remove") as mock_remove:
        
        mock_tts_instance = MagicMock()
        mock_gtts.return_value = mock_tts_instance
        
        tts = GTTSTTS()
        tts.speak("Teste")
        
        mock_gtts.assert_called_with(text="Teste", lang="pt", slow=False)
        mock_tts_instance.save.assert_called()
        mock_mixer.music.load.assert_called()
        mock_mixer.music.play.assert_called()
