# Assistente Virtual

## Visão Geral

Sistema de assistência virtual em um único arquivo `assistente.py` com reconhecimento de fala (speech to text), síntese de voz (text to speech) e execução de comandos utilitários: pesquisa na Wikipedia, pesquisa no YouTube e abertura da busca por farmácias próximas no Google Maps.

## Requisitos

- Python 3.11+ (testado em Windows)
- Microfone para modo voz (opcional; modo texto disponível)

## Instalação

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

Opcional para modo voz (se o microfone não for detectado): instalar PyAudio via wheel pré-compilado. Caso necessário, utilize um wheel compatível com seu Python e arquitetura disponível em repositórios de wheels para Windows.

## Configuração

- Arquivo `.env` já incluído. Ajuste conforme necessário:

```env
LANG=pt-BR
WAKE_WORD=assistente
STT_ENGINE=speech_recognition
TTS_ENGINE=pyttsx3
```

## Uso

- Modo voz:

```bash
.\.venv\Scripts\python assistente.py --mode voice
```

- Modo texto (sem microfone):

```bash
.\.venv\Scripts\python assistente.py --mode text
```

- Executar uma única vez com comando pré-definido:

```bash
.\.venv\Scripts\python assistente.py --mode text --once --command "wikipedia inteligência artificial"
```

### Exemplos de comandos

- "wikipedia linguagem python"
- "youtube música clássica"
- "preciso de uma farmácia"
- "sair" para encerrar

## Estrutura do Projeto

```
assistente.py
requirements.txt
.env
.env.example
.gitignore
README.md
```

## Execução dos Testes

Sem suíte de testes automatizada neste formato; a validação é manual via CLI.

## Detalhes Técnicos

- `SpeechRecognitionSTT` utiliza a API do Google via biblioteca SpeechRecognition.
- `Pyttsx3TTS` realiza síntese de voz local via pyttsx3 e tenta selecionar voz em português.
- `parse_and_execute` faz roteamento simples por palavras-chave para abrir Wikipedia, YouTube ou Google Maps.
- `Assistant` orquestra STT, TTS e execução das ações.

## Tratamento de Erros

- Falhas de microfone ou reconhecimento retornam mensagens adequadas e o sistema pode ser usado em modo texto.
- Comandos não reconhecidos retornam mensagem indicando erro e não encerram o programa.

## Licença

Uso educacional.
.### Notebook

- Abrir `assistente.ipynb` no Jupyter.
- O notebook foi gerado a partir de `assistente.py` via Jupytext e contém células Markdown explicando cada seção (STT, TTS, Ações, Orquestrador e CLI).
- Sincronizar alterações:

```bash
.\.venv\Scripts\python -m jupytext --to ipynb assistente.py
.\.venv\Scripts\python -m jupytext --to py assistente.ipynb
```