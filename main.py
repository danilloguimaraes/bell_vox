import os
import whisper
from flask import Flask, request, jsonify

app = Flask(__name__)
model = whisper.load_model("base")  # Modelo de transcrição do Whisper

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/transcribe", methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
