# Assistente Virtual com IA

> ⚠️ **Projeto em Desenvolvimento**: Este software está em fase ativa de construção e melhorias. Funcionalidades podem mudar e bugs podem ocorrer.

Este projeto implementa um assistente virtual capaz de ouvir comandos de voz, processá-los e responder usando fala.

## Funcionalidades

O projeto possui duas versões:

1.  **`assistente.py`**: Versão clássica leve.
    *   STT: Google Speech Recognition (Online)
    *   TTS: pyttsx3 (Offline)
    *   Comandos: Wikipedia, YouTube, Farmácia.

2.  **`assistente_ai.py`**: Versão avançada com IA para terminal.
    *   STT: OpenAI Whisper (Local, alta precisão)
    *   IA: OpenAI ChatGPT (Inteligência Geral)
    *   TTS: Google Text-to-Speech (gTTS, voz natural)
    *   Comandos: Wikipedia, YouTube, Farmácia + Conversação livre via ChatGPT.

3.  **`interface_gradio.py`** (NOVO): Interface visual moderna no navegador.
    *   Mesmas funcionalidades da versão IA, mas com interface gráfica.
    *   Suporte a entrada por áudio e texto simultaneamente.
    *   Histórico de conversa visual.

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

### Interface Visual (Gradio)

Para abrir a interface no seu navegador:
```bash
python interface_gradio.py
```

### Versão IA (Terminal)

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
- `interface_gradio.py`: Interface gráfica para o assistente de IA.
- `assistente.ipynb`: Versão em notebook do assistente original.
- `Assistente_de_Voz_Multi_Idiomas_Com_Whisper_e_ChatGPT.ipynb`: Notebook de referência tecnológica.
- `requirements.txt`: Lista de dependências.
- `README.md`: Este arquivo.
