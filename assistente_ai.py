# %% [markdown]
# Assistente Virtual com IA (Whisper + ChatGPT + gTTS)

# %%
import argparse
import os
import sys
import tempfile
import time
import urllib.parse
import webbrowser
from dataclasses import dataclass
from typing import Protocol, Optional, Iterable

from dotenv import load_dotenv

# Patch para compatibilidade com Python 3.13+
if sys.version_info >= (3, 13):
    import types
    sys.modules['aifc'] = types.ModuleType('aifc')
    sys.modules['audioop'] = types.ModuleType('audioop')

# Imports globais rápidos
import requests

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
    def __init__(self, model_size: str = "tiny", language: str = "pt", duration: int = 5):
        print(f"\n[WhisperSTT] Inicializando...")
        print(f"[WhisperSTT] Carregando bibliotecas de áudio e IA (isso pode demorar na primeira vez)...")
        
        # Lazy imports para não travar o início do script
        global whisper, sd, wav, np
        import whisper
        import sounddevice as sd
        import scipy.io.wavfile as wav
        import numpy as np

        print(f"[WhisperSTT] Carregando modelo Whisper '{model_size}'...")
        if not os.path.exists(os.path.expanduser(f"~/.cache/whisper/{model_size}.pt")):
             print(f"[WhisperSTT] AVISO: Baixando modelo '{model_size}'. Isso pode levar alguns minutos dependendo da sua internet.")
        
        try:
            self._model = whisper.load_model(model_size)
            print("[WhisperSTT] Modelo carregado com sucesso.")
        except Exception as e:
            print(f"[WhisperSTT] ERRO CRÍTICO ao carregar modelo: {e}")
            print("Verifique se o FFmpeg está instalado e no PATH do sistema.")
            raise e

        self._language = language
        self._duration = duration

    def listen(self, timeout: Optional[float] = None) -> Optional[str]:
        duration = timeout if timeout is not None else self._duration
        fs = 44100  # Sample rate
        
        print(f"\n[Ouvindo] Fale agora ({duration}s)...")
        try:
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()
            print("[Processando] Transcrevendo áudio...")

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                temp_filename = f.name
            
            wav.write(temp_filename, fs, recording)

            # Transcrever
            result = self._model.transcribe(temp_filename, language=self._language, fp16=False)
            text = result["text"].strip()

            try:
                os.remove(temp_filename)
            except OSError:
                pass

            return text if text else None

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
            return input("\nDigite um comando (ou 'sair'): ").strip()
        except EOFError:
            return None


class GTTSTTS:
    def __init__(self, language: str = "pt"):
        self._language = language
        # Lazy import
        global gTTS, pygame
        try:
            from gtts import gTTS
            import pygame
            pygame.mixer.init()
        except Exception as e:
            print(f"Aviso: Erro ao inicializar áudio: {e}")

    def speak(self, text: str) -> None:
        if not text:
            return
        
        try:
            tts = gTTS(text=text, lang=self._language, slow=False)
            
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_filename = f.name
            
            tts.save(temp_filename)

            print(f"\n🤖 Assistente: {text}")
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.unload()
            
            try:
                os.remove(temp_filename)
            except OSError:
                pass
                
        except Exception as e:
            print(f"Erro no TTS: {e}")
            print(f"🤖 Assistente (texto): {text}")


class ChatGPTIntelligence:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        global openai
        import openai
        self._client = openai.OpenAI(api_key=api_key)
        self._model = model

    def process(self, text: str) -> str:
        if not text:
            return "Não entendi."
        
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
            return f"Erro na IA: {str(e)}"


# %% [markdown]
# Ações Locais

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
        return ActionResult(True, f"Pesquisando '{query}' na Wikipedia", True)
        
    if "youtube" in s or "vídeo" in s or "video" in s:
        query = s.replace("youtube", "").replace("vídeo", "").replace("video", "").replace("pesquisar", "").strip()
        if not query:
            return ActionResult(False, "O que devo pesquisar no YouTube?", True)
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query)
        webbrowser.open(url)
        return ActionResult(True, f"Pesquisando '{query}' no YouTube", True)
        
    if "farmácia" in s or "farmacia" in s:
        url = "https://www.google.com/maps/search/farmacia+perto+de+mim"
        webbrowser.open(url)
        return ActionResult(True, "Abrindo mapa de farmácias", True)

    return None


# %% [markdown]
# Orquestrador

class AIAssistant:
    def __init__(self, stt: SpeechToText, tts: TextToSpeech, ai: Optional[Intelligence]):
        self._stt = stt
        self._tts = tts
        self._ai = ai

    def run(self):
        print("\n--- Assistente Pronto ---")
        self._tts.speak("Olá! Como posso ajudar?")
        
        while True:
            text = self._stt.listen()
            
            if not text:
                continue
                
            print(f"🎤 Você: {text}")
            
            if text.lower().strip() in {"sair", "encerrar", "exit", "tchau"}:
                self._tts.speak("Até logo!")
                break

            local_result = try_local_commands(text)
            if local_result:
                self._tts.speak(local_result.message)
                continue

            if self._ai:
                response = self._ai.process(text)
                self._tts.speak(response)
            else:
                self._tts.speak("Comando não reconhecido. (IA não configurada)")


# %% [markdown]
# Configuração e Main

def parse_args():
    p = argparse.ArgumentParser("Assistente AI")
    p.add_argument("--mode", choices=["voice", "text"], default="voice", help="Modo de entrada")
    p.add_argument("--no-ai", action="store_true", help="Desativar ChatGPT")
    p.add_argument("--duration", type=int, default=5, help="Duração da gravação (segundos)")
    p.add_argument("--model", type=str, default="tiny", help="Modelo Whisper (tiny, base, small, medium, large)")
    return p.parse_args()

def check_ffmpeg():
    import shutil
    if not shutil.which("ffmpeg"):
        print("\n[ERRO] FFmpeg não encontrado!")
        print("O Whisper precisa do FFmpeg para funcionar.")
        print("Instale e adicione ao PATH: https://ffmpeg.org/download.html")
        print("Windows: 'choco install ffmpeg' ou baixe o executável.\n")
        # Não abortar hard, mas avisar

def main():
    print(">>> Iniciando Assistente Virtual...")
    load_dotenv()
    args = parse_args()
    
    check_ffmpeg()

    # Configurar TTS
    tts = GTTSTTS(language="pt")

    # Configurar STT
    if args.mode == "voice":
        stt = WhisperSTT(model_size=args.model, language="pt", duration=args.duration)
    else:
        stt = TextInputSTT()

    # Configurar IA
    ai = None
    if not args.no_ai:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "sua_chave_api_aqui":
            print(f"[IA] Chave OpenAI detectada.")
            ai = ChatGPTIntelligence(api_key=api_key)
        else:
            print("\n[AVISO] Chave OpenAI não configurada (OPENAI_API_KEY).")
            print("Apenas comandos locais (Wikipedia, YouTube) funcionarão.")
            print("Para ativar a IA, configure o arquivo .env.\n")
    
    # Iniciar
    assistant = AIAssistant(stt, tts, ai)
    assistant.run()

if __name__ == "__main__":
    main()
