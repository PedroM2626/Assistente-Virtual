# Assistente Virtual com IA

> ⚠️ **Projeto em Desenvolvimento**: Este software está em fase ativa de construção e melhorias. Funcionalidades podem mudar e bugs podem ocorrer.

Este projeto implementa um assistente virtual capaz de ouvir comandos de voz, processá-los e responder usando fala. O foco atual é a operação **100% local**, garantindo privacidade e custo zero.

## 🚀 Demonstração Online
O projeto está hospedado e pode ser testado no Hugging Face Spaces:
🔗 [**Virtual Assistent no Hugging Face**](https://huggingface.co/spaces/PedroM2626/virtual-assistent)

## Funcionalidades

O projeto possui três versões principais:

1.  **`app.py`**: Interface visual moderna no navegador (Gradio) - **Recomendado**.
    *   **100% Local**: Não requer chaves de API externas.
    *   STT: OpenAI Whisper (**Local e Gratuito** - Modelo `base`).
    *   TTS: Google Text-to-Speech (gTTS).
    *   Interface gráfica intuitiva com histórico de conversa.
    *   Comandos locais: Wikipedia, YouTube, Google Maps.

2.  **`assistente_ai.py`**: Versão avançada para terminal.
    *   STT: OpenAI Whisper (**Local e Gratuito**).
    *   IA: OpenAI ChatGPT (Opcional, requer chave API).
    *   TTS: Google Text-to-Speech (gTTS).
    *   Comandos locais + Conversação livre via ChatGPT.

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
4.  Configure as variáveis de ambiente (Opcional):
    *   Copie `.env.example` para `.env`
    *   Adicione sua `OPENAI_API_KEY` apenas se for usar a versão `assistente_ai.py` com ChatGPT.

## Como Usar

### Interface Visual (Gradio)
Esta é a versão principal e 100% local.
```bash
python app.py
```

### Versão Terminal (IA)
Para usar voz (padrão):
```bash
python assistente_ai.py
```

### Versão Clássica
```bash
python assistente.py
```

## Estrutura do Projeto

- `app.py`: Interface gráfica principal (Gradio).
- `assistente_ai.py`: Script de terminal com integração Whisper/ChatGPT.
- `assistente.py`: Script original leve.
- `assistente.ipynb`: Notebook com demonstração e experimentação.
- `requirements.txt`: Lista de dependências.
- `README.md`: Este arquivo.
