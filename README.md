# Assistente Virtual com IA


Este projeto implementa um assistente virtual capaz de ouvir comandos de voz, processá-los e responder usando fala. Agora integrado com a inteligência artificial **GLM-4.7-Flash** via Hugging Face.

## 🚀 Demonstração Online
O projeto está hospedado e pode ser testado no Hugging Face Spaces:
🔗 [**Virtual Assistent no Hugging Face**](https://huggingface.co/spaces/PedroM2626/virtual-assistent)

## Funcionalidades

O projeto possui três versões principais:

1.  **`app.py`**: Interface visual moderna no navegador (Gradio) - **Recomendado**.
    *   **Voz Local**: STT com OpenAI Whisper (**Local e Gratuito** - Modelo `base`).
    *   **Inteligência Híbrida**: Usa **GLM-4.7-Flash** para respostas inteligentes via Hugging Face API.
    *   TTS: Google Text-to-Speech (gTTS).
    *   Interface gráfica intuitiva com histórico de conversa.
    *   Comandos locais: Wikipedia, YouTube, Google Maps.

2.  **`assistente_ai.py`**: Versão avançada para terminal (Legado).
    *   STT: OpenAI Whisper (**Local e Gratuito**).
    *   IA: OpenAI ChatGPT (Opcional).
    *   TTS: Google Text-to-Speech (gTTS).

3.  **`assistente.py`**: Versão clássica leve.
    *   STT: Google Speech Recognition (Online) ou Whisper Local.
    *   TTS: pyttsx3 (Offline).
    *   Comandos básicos: Wikipedia, YouTube, Farmácia.

## Pré-requisitos

- Python 3.8+
- **FFmpeg**: Necessário para o Whisper e manipulação de áudio.
    - **Windows**: Baixe do [site oficial](https://ffmpeg.org/download.html) ou use `choco install ffmpeg`. Adicione ao PATH.
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
    *   Adicione seu `HF_TOKEN` (Hugging Face Token) no arquivo `.env` para habilitar a inteligência artificial.

## Como Usar

### Interface Visual (Gradio)
Esta é a versão principal com IA integrada.
```bash
python app.py
```

### Versão Terminal
```bash
python assistente_ai.py
```

### Versão Clássica
```bash
python assistente.py
```

## Estrutura do Projeto

- `app.py`: Interface gráfica principal (Gradio) com integração GLM-4.7-Flash.
- `assistente_ai.py`: Script de terminal.
- `assistente.py`: Script original leve.
- `requirements.txt`: Lista de dependências.
- `README.md`: Este arquivo.
