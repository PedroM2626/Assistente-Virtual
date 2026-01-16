import os
import sys
import tempfile
import time
import urllib.parse
import webbrowser
import gradio as gr
from dotenv import load_dotenv

# Patch para compatibilidade com Python 3.13+
if sys.version_info >= (3, 13):
    import types
    sys.modules['aifc'] = types.ModuleType('aifc')
    sys.modules['audioop'] = types.ModuleType('audioop')

# Lazy imports para o Whisper e gTTS
whisper_model = None

def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        import whisper
        print("Carregando modelo Whisper (Local e Gratuito)...")
        whisper_model = whisper.load_model("base")
    return whisper_model

def get_chatgpt_response(text, api_key):    
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente virtual útil e conciso. Responda em português."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {str(e)}"

def try_local_commands(text):
    s = (text or "").lower()
    if "wikipedia" in s:
        query = s.replace("wikipedia", "").replace("pesquisar", "").strip()
        if not query:
            return "O que devo pesquisar na Wikipedia?"
        url = "https://pt.wikipedia.org/wiki/Special:Search?search=" + urllib.parse.quote_plus(query)
        webbrowser.open(url)
        return f"Pesquisando '{query}' na Wikipedia."
        
    if "youtube" in s or "vídeo" in s or "video" in s:
        query = s.replace("youtube", "").replace("vídeo", "").replace("video", "").replace("pesquisar", "").strip()
        if not query:
            return "O que devo pesquisar no YouTube?"
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query)
        webbrowser.open(url)
        return f"Pesquisando '{query}' no YouTube."
        
    if "farmácia" in s or "farmacia" in s:
        webbrowser.open("https://www.google.com/maps/search/farmacia+perto+de+mim")
        return "Abrindo mapa de farmácias próximas."

    return None

def text_to_speech(text):
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='pt')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        print(f"Erro TTS: {e}")
        return None

def process_interaction(audio_path, text_input, history, api_key):
    # Inicializar histórico se for None
    if history is None:
        history = []
        
    # Determinar a entrada (áudio ou texto)
    input_text = ""
    
    try:
        if audio_path:
            print(f"Processando áudio de: {audio_path}")
            model = get_whisper_model()
            result = model.transcribe(audio_path, language="pt", fp16=False)
            input_text = result["text"].strip()
            print(f"Transcrição Whisper: {input_text}")
        elif text_input:
            input_text = text_input
            print(f"Entrada de texto: {input_text}")
        
        if not input_text:
            return history, "", gr.update()

        # Processar comando local primeiro
        response_text = try_local_commands(input_text)
        
        # Se não for comando local, tentar IA
        if response_text is None:
            response_text = get_chatgpt_response(input_text, api_key)
            
            # Se a IA não estiver disponível (sem chave), apenas confirma o que ouviu
            if response_text is None:
                response_text = f"Você disse: {input_text}"
        
        print(f"Resposta: {response_text}")

        # Gerar áudio
        audio_response = text_to_speech(response_text)
        
        # Atualizar histórico (Gradio 4+ prefere lista de dicts ou lista de listas)
        history.append({"role": "user", "content": input_text})
        history.append({"role": "assistant", "content": response_text})
        
        return history, "", audio_response if audio_response else gr.update()

    except Exception as e:
        error_msg = f"Erro no processamento: {str(e)}"
        print(error_msg)
        history.append({"role": "user", "content": input_text if input_text else "???"})
        history.append({"role": "assistant", "content": error_msg})
        return history, "", gr.update()

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "")
    
    with gr.Blocks(title="Assistente Virtual Local") as demo:
        gr.Markdown("# 🤖 Assistente Virtual 100% Local")
        gr.Markdown("Este assistente usa **OpenAI Whisper** rodando localmente no seu computador para ouvir e processar comandos sem depender de APIs externas.")
        
        gr.Markdown("### 🎤 Comandos Disponíveis:")
        gr.Markdown("- 'Pesquisar Wikipedia sobre [assunto]'")
        gr.Markdown("- 'Abrir YouTube' ou 'Vídeo de [assunto]'")
        gr.Markdown("- 'Farmácia próxima'")
        
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label="Conversa")
                audio_output = gr.Audio(label="Resposta em Áudio", autoplay=True)
            
            with gr.Column(scale=1):
                audio_input = gr.Audio(label="Fale aqui", type="filepath")
                text_input = gr.Textbox(label="Ou digite aqui", placeholder="Ex: Pesquisar Wikipedia sobre Python")
                btn_send = gr.Button("Enviar", variant="primary")
                btn_clear = gr.Button("Limpar Conversa")

        # Estado para a chave API (pega do .env inicialmente)
        api_key_state = gr.State(value=api_key)

        # Eventos
        btn_send.click(
            process_interaction, 
            inputs=[audio_input, text_input, chatbot, api_key_state], 
            outputs=[chatbot, text_input, audio_output]
        )
        
        text_input.submit(
            process_interaction, 
            inputs=[audio_input, text_input, chatbot, api_key_state], 
            outputs=[chatbot, text_input, audio_output]
        )

        btn_clear.click(lambda: ([], "", gr.update(value=None)), None, [chatbot, text_input, audio_output])

    demo.launch(share=True)

if __name__ == "__main__":
    main()
