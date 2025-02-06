import io
import os
import openai
import whisper
from flask import Flask, request, jsonify
from openai import api_key

app = Flask(__name__)
model = whisper.load_model("base")  # Modelo de transcrição do Whisper

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/offline", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    print(f"Arquivo salvo em: {filepath}")

    # Transcrevendo o áudio
    result = model.transcribe(filepath)

    return jsonify({"transcription": result["text"]})

# Solicita a transcião de um texto para a API do Whisper da OpenAI
@app.route("/whisper", methods=["POST"])
def transcribe_with_whisper():
    # Read the api key from the request form
    openai.api_key = request.form.get("openai.api_key")
    whisperClient = openai.OpenAI(api_key=openai.api_key)

    # Verifica se um arquivo foi enviado
    if "audio" not in request.files:
        return jsonify({"error": "Nenhum arquivo de áudio enviado"}), 400

    # Obtém o arquivo de áudio da requisição
    audio_file = request.files["audio"]

    try:
        # Converte para formato correto e mantém a extensão
        audio_bytes = io.BytesIO(audio_file.read())

        # Mantém a extensão correta do arquivo
        audio_tuple = (audio_file.filename, audio_bytes, audio_file.content_type)

        # Enviar para o Whisper
        transcription = whisperClient.audio.transcriptions.create(
            model="whisper-1",
            file=audio_tuple
        )

        return jsonify({"transcription": transcription.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Disponibiliza uma página com formulário para envio de arquivos para transcrição offline
@app.route("/transcricao-offline", methods=["GET"])
def index():
    return """
    <html>
        <body>
            <h1>Transcrição de áudio</h1>
            <form action="/offline" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Enviar">
            </form>
        </body>
    </html>
    """

# Disponibiliza uma página com formulário para envio de arquivos para transcrição com Whisper
@app.route("/transcricao-whisper", methods=["GET"])
def whisper_index():
    return """
    <html>
        <body>
            <h1>Transcrição de áudio com Whisper</h1>
            <form action="/whisper" method="post" enctype="multipart/form-data">
                <input type="file" name="audio">
                <input type="text" name="openai.api_key" placeholder="API Key">
                <input type="submit" value="Enviar">
            </form>
        </body>
    </html>
    """

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify(
        {
            "name": "Bell Vox",
            "status": "ok"
        })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
