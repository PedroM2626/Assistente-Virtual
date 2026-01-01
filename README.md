# Assistente Virtual com IA

> ⚠️ **Projeto em Desenvolvimento**: Este software está em fase ativa de construção e melhorias. Funcionalidades podem mudar e bugs podem ocorrer.

Este projeto implementa um assistente virtual capaz de ouvir comandos de voz, processá-los e responder usando fala.

## Funcionalidades

O projeto possui duas versões:

1.  **`assistente.py`**: Versão clássica leve.
    *   STT: Google Speech Recognition (Online)
    *   TTS: pyttsx3 (Offline)
    *   Comandos: Wikipedia, YouTube, Farmácia.

2.  **`assistente_ai.py`** (NOVO): Versão avançada com IA.
    *   STT: OpenAI Whisper (Local, alta precisão)
    *   IA: OpenAI ChatGPT (Inteligência Geral)
    *   TTS: Google Text-to-Speech (gTTS, voz natural)
    *   Comandos: Wikipedia, YouTube, Farmácia + Conversação livre via ChatGPT.

## Pré-requisitos

- Python 3.8+
- Conta na OpenAI (para usar o ChatGPT)
- **FFmpeg**: Necessário para o Whisper e manipulação de áudio.
    - **Windows**: Baixe do [site oficial](https://ffmpeg.org/download.html) ou use `choco install ffmpeg` se tiver o Chocolatey. Adicione ao PATH.
    - **Linux**: `sudo apt install ffmpeg`
    - **Mac**: `brew install ffmpeg`

## Instalação

1.  Clone o repositório.
2.  Crie um ambiente virtual:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure as variáveis de ambiente:
    *   Copie `.env.example` para `.env`
    *   Edite `.env` e adicione sua `OPENAI_API_KEY` se for usar o modo IA.

## Como Usar

### Versão IA (Recomendada)

Para usar voz (padrão):
```bash
python assistente_ai.py
```

Para usar texto (sem microfone):
```bash
python assistente_ai.py --mode text
```

Para desativar a IA (economizar custos) e usar apenas comandos locais com Whisper:
```bash
python assistente_ai.py --no-ai
```

### Versão Clássica

```bash
python assistente.py
```

## Estrutura do Projeto

- `assistente.py`: Script original.
- `assistente_ai.py`: Script novo com integração Whisper/ChatGPT.
- `requirements.txt`: Lista de dependências.
- `README.md`: Este arquivo.
