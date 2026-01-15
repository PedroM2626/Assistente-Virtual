# %% [markdown]
# Assistente Virtual
#
# Notebook/Script único com:
# - STT (Speech to Text)
# - TTS (Text to Speech)
# - Comandos: Wikipedia, YouTube, Farmácia próxima

# %%
import argparse
from typing import Protocol, Optional, Iterable
from dataclasses import dataclass
import os
import urllib.parse
import webbrowser
from dotenv import load_dotenv


class SpeechToText(Protocol):
    def listen(self, timeout: Optional[float] = None) -> Optional[str]:
        pass


class TextToSpeech(Protocol):
    def speak(self, text: str) -> None:
        pass


# %% [markdown]
# Implementações de STT e TTS

class SpeechRecognitionSTT:
    def __init__(self, language: str = "pt-BR"):
        try:
            import speech_recognition as sr
            self._sr = sr
            self._rec = sr.Recognizer()
            self._language = language
        except ImportError:
            print("Erro: speech_recognition não instalado. Use 'pip install SpeechRecognition'")
            raise

    def listen(self, timeout: Optional[float] = None) -> Optional[str]:
        print("\n[Ouvindo...] Fale agora.")
        try:
            with self._sr.Microphone() as source:
                self._rec.adjust_for_ambient_noise(source)
                audio = self._rec.listen(source, timeout=timeout)
            print("[Processando...]")
            text = self._rec.recognize_google(audio, language=self._language)
            return text
        except Exception as e:
            print(f"Erro no reconhecimento: {e}")
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


class Pyttsx3TTS:
    def __init__(self, language: str = "pt-BR", rate: Optional[int] = None):
        try:
            import pyttsx3
            self._engine = pyttsx3.init()
            self._language = language
            if rate is not None:
                self._engine.setProperty("rate", rate)
            self._select_voice()
        except ImportError:
            print("Erro: pyttsx3 não instalado. Use 'pip install pyttsx3'")
            self._engine = None

    def _select_voice(self) -> None:
        if not self._engine: return
        voices = self._engine.getProperty("voices")
        chosen = None
        for v in voices:
            name = getattr(v, "name", "") or ""
            lang = "".join(getattr(v, "languages", []) or [])
            if self._language.lower()[:2] in (lang.lower(), name.lower()):
                chosen = v.id
                break
        if chosen:
            self._engine.setProperty("voice", chosen)

    def speak(self, text: str) -> None:
        print(f"🤖 Assistente: {text}")
        if self._engine:
            try:
                self._engine.say(text)
                self._engine.runAndWait()
            except Exception as e:
                print(f"(Erro no áudio: {e})")


class SilentTTS:
    def speak(self, text: str) -> None:
        print(f"🤖 Assistente (silencioso): {text}")


# %% [markdown]
# Configuração por variáveis de ambiente

@dataclass
class Config:
    lang: str = "pt-BR"
    wake_word: str = "assistente"
    stt_engine: str = "speech_recognition"
    tts_engine: str = "pyttsx3"


def load_config() -> Config:
    return Config(
        lang=os.getenv("LANG", "pt-BR"),
        wake_word=os.getenv("WAKE_WORD", "assistente"),
        stt_engine=os.getenv("STT_ENGINE", "speech_recognition"),
        tts_engine=os.getenv("TTS_ENGINE", "pyttsx3"),
    )


# %% [markdown]
# Ações: Wikipedia, YouTube e Farmácia

@dataclass
class ActionResult:
    success: bool
    message: str


def open_wikipedia(query: str) -> ActionResult:
    if not query:
        return ActionResult(False, "Nenhuma consulta fornecida")
    url = "https://pt.wikipedia.org/wiki/Special:Search?search=" + urllib.parse.quote_plus(query)
    webbrowser.open(url)
    return ActionResult(True, f"Abrindo pesquisa na Wikipedia para '{query}'")


def open_youtube(query: str) -> ActionResult:
    if not query:
        return ActionResult(False, "Nenhuma consulta fornecida")
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query)
    webbrowser.open(url)
    return ActionResult(True, f"Abrindo pesquisa no YouTube para '{query}'")


def find_nearest_pharmacy() -> ActionResult:
    url = "https://www.google.com/maps/search/farmacia+perto+de+mim"
    webbrowser.open(url)
    return ActionResult(True, "Abrindo pesquisa de farmácia mais próxima")


def parse_and_execute(text: str) -> ActionResult:
    s = (text or "").lower()
    if not s:
        return ActionResult(False, "Nenhum texto reconhecido")
    if "wikipedia" in s:
        q = s.replace("wikipedia", "").replace("pesquisar", "").strip()
        return open_wikipedia(q or "")
    if "youtube" in s or "vídeo" in s or "video" in s:
        q = s.replace("youtube", "").replace("vídeo", "").replace("video", "").replace("pesquisar", "").strip()
        return open_youtube(q or "")
    if "farmácia" in s or "farmacia" in s:
        return find_nearest_pharmacy()
    return ActionResult(False, "Comando não reconhecido")


# %% [markdown]
# Orquestrador do Assistente

class Assistant:
    def __init__(self, stt: SpeechToText, tts: TextToSpeech, config: Config):
        self._stt = stt
        self._tts = tts
        self._config = config

    def run_once(self, text_override: Optional[str] = None) -> ActionResult:
        text = text_override if text_override is not None else self._stt.listen()
        print(f"🎤 Você: {text}")
        result = parse_and_execute(text or "")
        self._tts.speak(result.message)
        return result

    def run(self) -> None:
        self._tts.speak("Olá! Diga um comando.")
        while True:
            text = self._stt.listen()
            if text is None:
                self._tts.speak("Não entendi")
                continue
            
            print(f"🎤 Você: {text}")
            
            if text.lower().strip() in {"sair", "encerrar", "exit", "tchau"}:
                self._tts.speak("Até logo!")
                break
            
            result = parse_and_execute(text)
            self._tts.speak(result.message)


def build_assistant(mode: str, once_text: str | None) -> Assistant:
    cfg = load_config()
    
    # Selecionar TTS
    try:
        tts = Pyttsx3TTS(language=cfg.lang)
    except Exception:
        tts = SilentTTS()

    # Selecionar STT
    if mode == "voice":
        try:
            stt = SpeechRecognitionSTT(language=cfg.lang)
        except Exception:
            print("Falha ao iniciar microfone. Alternando para modo texto.")
            stt = TextInputSTT([once_text] if once_text else None)
    else:
        stt = TextInputSTT([once_text] if once_text else None)
        
    return Assistant(stt=stt, tts=tts, config=cfg)


# %% [markdown]
# Interface de Linha de Comando (CLI)

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser("Assistente Virtual")
    p.add_argument("--mode", choices=["voice", "text"], default="voice")
    p.add_argument("--once", action="store_true")
    p.add_argument("--command", type=str, default=None)
    return p.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    assistant = build_assistant(args.mode, args.command)
    if args.once:
        assistant.run_once(args.command)
    else:
        assistant.run()


if __name__ == "__main__":
    main()
