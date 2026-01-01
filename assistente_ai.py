# %% [markdown]
# Assistente Virtual com IA (Whisper + ChatGPT + gTTS)
#
# Baseado no notebook Assistente_de_Voz_Multi_Idiomas_Com_Whisper_e_ChatGPT.ipynb
# Integra:
# - STT: OpenAI Whisper (Local)
# - IA: OpenAI ChatGPT (API)
# - TTS: Google Text-to-Speech (gTTS)
# - Comandos Locais: Wikipedia, YouTube, etc.

# %%
import argparse
import os
import tempfile
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass
from typing import Protocol, Optional, Iterable

from dotenv import load_dotenv

# Dependências externas
import speech_recognition as sr
import whisper
import openai
from gtts import gTTS
import pygame


# %% [markdown]
# Protocolos

class SpeechToText(Protocol):
    def listen(self, timeout: Optional[float] = None) -> Optional[str]:
        pass


class TextToSpeech(Protocol):
    def speak(self, text: str) -> None:
        pass


class Intelligence(Protocol):
    def process(self, text: str) -> str:
        pass


# %% [markdown]
# Implementações

class WhisperSTT:
    def __init__(self, model_size: str = "base", language: str = "pt"):
        print(f"Carregando modelo Whisper '{model_size}'...")
        self._model = whisper.load_model(model_size)
        self._language = language
        self._recognizer = sr.Recognizer()
        print("Modelo Whisper carregado.")

    def listen(self, timeout: Optional[float] = None) -> Optional[str]:
        try:
            with sr.Microphone() as source:
                print("Ouvindo (Whisper)...")
                self._recognizer.adjust_for_ambient_noise(source)
                audio = self._recognizer.listen(source, timeout=timeout)

            # Salvar áudio temporário para o Whisper processar
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio.get_wav_data())
                temp_filename = f.name

            # Transcrever
            result = self._model.transcribe(temp_filename, language=self._language, fp16=False)
            text = result["text"].strip()

            # Limpar arquivo temporário
            try:
                os.remove(temp_filename)
            except OSError:
                pass

            return text if text else None

        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Erro no WhisperSTT: {e}")
            return None


class TextInputSTT:
    def __init__(self, inputs: Optional[Iterable[str]] = None):
        self._inputs = list(inputs) if inputs is not None else None

    def listen(self, timeout: Optional[float] = None) -> Optional[str]:
        if self._inputs is not None:
            if not self._inputs:
                return None
            return self._inputs.pop(0)
        try:
            return input("Digite um comando (ou 'sair'): ").strip()
        except EOFError:
            return None


class GTTSTTS:
    def __init__(self, language: str = "pt"):
        self._language = language
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Aviso: Não foi possível inicializar pygame mixer: {e}")

    def speak(self, text: str) -> None:
        if not text:
            return
        
        try:
            # Gerar áudio
            tts = gTTS(text=text, lang=self._language, slow=False)
            
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_filename = f.name
                # Fechar o arquivo para que o gTTS possa salvar (Windows lock)
            
            tts.save(temp_filename)

            # Reproduzir
            print(f"Assistente: {text}")
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.unload()
            
            # Limpar
            try:
                os.remove(temp_filename)
            except OSError:
                pass
                
        except Exception as e:
            print(f"Erro no GTTSTTS: {e}")
            # Fallback print
            print(f"Fala (erro áudio): {text}")


class ChatGPTIntelligence:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self._client = openai.OpenAI(api_key=api_key)
        self._model = model

    def process(self, text: str) -> str:
        if not text:
            return "Não entendi o que você disse."
        
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": "Você é um assistente virtual útil e conciso. Responda em português."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro ao contatar a IA: {str(e)}"


# %% [markdown]
# Ações Locais (Híbrido)

@dataclass
class ActionResult:
    success: bool
    message: str
    handled_locally: bool


def try_local_commands(text: str) -> Optional[ActionResult]:
    s = (text or "").lower()
    
    if "wikipedia" in s:
        query = s.replace("wikipedia", "").replace("pesquisar", "").strip()
        if not query:
            return ActionResult(False, "O que devo pesquisar na Wikipedia?", True)
        url = "https://pt.wikipedia.org/wiki/Special:Search?search=" + urllib.parse.quote_plus(query)
        webbrowser.open(url)
        return ActionResult(True, f"Abrindo Wikipedia para '{query}'", True)
        
    if "youtube" in s or "vídeo" in s or "video" in s:
        query = s.replace("youtube", "").replace("vídeo", "").replace("video", "").replace("pesquisar", "").strip()
        if not query:
            return ActionResult(False, "O que devo pesquisar no YouTube?", True)
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query)
        webbrowser.open(url)
        return ActionResult(True, f"Abrindo YouTube para '{query}'", True)
        
    if "farmácia" in s or "farmacia" in s:
        url = "https://www.google.com/maps/search/farmacia+perto+de+mim"
        webbrowser.open(url)
        return ActionResult(True, "Procurando farmácias próximas", True)

    return None


# %% [markdown]
# Orquestrador

class AIAssistant:
    def __init__(self, stt: SpeechToText, tts: TextToSpeech, ai: Optional[Intelligence]):
        self._stt = stt
        self._tts = tts
        self._ai = ai

    def run(self):
        self._tts.speak("Olá, sou seu assistente com Inteligência Artificial. Como posso ajudar?")
        
        while True:
            text = self._stt.listen()
            
            if not text:
                continue
                
            print(f"Você disse: {text}")
            
            if text.lower().strip() in {"sair", "encerrar", "exit", "tchau"}:
                self._tts.speak("Até logo!")
                break

            # 1. Tentar comandos locais primeiro
            local_result = try_local_commands(text)
            if local_result:
                self._tts.speak(local_result.message)
                continue

            # 2. Se não for comando local, usar IA
            if self._ai:
                response = self._ai.process(text)
                self._tts.speak(response)
            else:
                self._tts.speak("Comando não reconhecido e IA não configurada.")


# %% [markdown]
# Configuração e Main

def parse_args():
    p = argparse.ArgumentParser("Assistente AI")
    p.add_argument("--mode", choices=["voice", "text"], default="voice", help="Modo de entrada")
    p.add_argument("--no-ai", action="store_true", help="Desativar ChatGPT (somente comandos locais)")
    return p.parse_args()

def main():
    load_dotenv()
    args = parse_args()

    # Configurar TTS
    # Poderíamos usar pyttsx3 como fallback, mas o pedido foi usar a tecnologia do notebook (gTTS)
    tts = GTTSTTS(language="pt")

    # Configurar STT
    if args.mode == "voice":
        # Verifica se ffmpeg está disponível (necessário para Whisper)
        # Assumimos que o usuário tem, ou o script falhará com erro descritivo do whisper
        stt = WhisperSTT(model_size="base", language="pt")
    else:
        stt = TextInputSTT()

    # Configurar IA
    ai = None
    if not args.no_ai:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "sua_chave_api_aqui":
            ai = ChatGPTIntelligence(api_key=api_key)
        else:
            print("AVISO: OPENAI_API_KEY não configurada. IA desativada.")
    
    # Iniciar
    assistant = AIAssistant(stt, tts, ai)
    assistant.run()

if __name__ == "__main__":
    main()
