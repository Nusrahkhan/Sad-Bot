from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from groq import Groq
from elevenlabs import generate, set_api_key, Voice, VoiceSettings
from dotenv import load_dotenv
from transformers import pipeline
import torch, os, base64, uuid, tempfile, requests, random

# Setup
app = Flask(__name__)
CORS(app)
load_dotenv()

# API keys
# API keys
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
set_api_key(os.getenv("ELEVEN_API_KEY"))  # Initialize ElevenLabs this way instead
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")


def text_to_speech(text):
    try:
        audio = generate(
            text=text,
            voice=Voice(
                voice_id="pNInz6obpgDQGcFmaJgB",
                settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
            ),
            model="eleven_monolingual_v1"
        )
        file = f"temp_{uuid.uuid4()}.mp3"
        with open(file, "wb") as f:
            f.write(audio)
        with open(file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        os.remove(file)
        return encoded
    except Exception as e:
        print("TTS error:", e)
        return None

# Load Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
whisper_model = pipeline("automatic-speech-recognition", model="openai/whisper-base", device=device)

# Roast via LLaMA3
def get_emotional_response(prompt):
    res = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": "Make a very emotional comment on them."},
                  {"role": "user", "content": prompt}],
        temperature=1.0,
        max_tokens=250
    )
    return res.choices[0].message.content

# Text-to-Speech
def text_to_speech(text):
    try:
        audio = generate(
            text=text,
            voice=Voice(
                voice_id="pNInz6obpgDQGcFmaJgB",
                settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
            ),
            model="eleven_monolingual_v1"
        )
        file = f"temp_{uuid.uuid4()}.mp3"
        with open(file, "wb") as f: f.write(audio)
        with open(file, "rb") as f: encoded = base64.b64encode(f.read()).decode("utf-8")
        os.remove(file)
        return encoded
    except Exception as e:
        print("TTS error:", e)
        return None


# Routes
@app.route('/emotional', methods=['POST'])
def emotional():
    try:
        data = request.json
        user_input = data.get("text", "")
        prompt = f"A very emotional comment on this:\n{user_input}\nMake them sob."
        
        # Get emotional response
        response = get_emotional_response(prompt)
        
        # Get audio
        audio = text_to_speech(response)
        
        return jsonify({
            "emotional": response,
            "audio": audio,
            "success": True
        })
    except Exception as e:
        print("Error in emotional route:", e)
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400
    audio = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        audio.save(f.name)
        text = whisper_model(f.name)["text"]
    os.unlink(f.name)
    return jsonify({'transcription': text})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
