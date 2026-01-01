from flask import Flask, request, jsonify, render_template, send_file
from dotenv import load_dotenv
from assistente import parse_and_execute, load_config
import os
import uuid
import tempfile

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    success = None
    if request.method == "POST":
        text = request.form.get("text", "")
        result = parse_and_execute(text)
        message = result.message
        success = result.success
        return render_template("index.html", message=message, success=success, last_text=text)
    return render_template("index.html", message=message, success=success, last_text="")

@app.route("/api/execute", methods=["POST"])
def api_execute():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", ""))
    result = parse_and_execute(text)
    return jsonify({"success": result.success, "message": result.message})

@app.route("/api/tts", methods=["POST"])
def api_tts():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", ""))
    if not text.strip():
        return jsonify({"success": False, "message": "Texto vazio"}), 400
    tts_dir = os.path.join(os.path.dirname(__file__), "static", "tts")
    os.makedirs(tts_dir, exist_ok=True)
    file_id = uuid.uuid4().hex
    wav_path = os.path.join(tts_dir, f"{file_id}.wav")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, wav_path)
        engine.runAndWait()
    except Exception:
        return jsonify({"success": False, "message": "Falha ao gerar áudio"}), 500
    return send_file(wav_path, mimetype="audio/wav")


def create_app() -> Flask:
    load_dotenv()
    _ = load_config()
    return app

if __name__ == "__main__":
    load_dotenv()
    _ = load_config()
    app.run(host="127.0.0.1", port=8000)