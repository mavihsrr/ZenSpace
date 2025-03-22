from flask import Flask, request, jsonify, send_file
import os
import edge_tts
import asyncio
import tempfile
import speech_recognition as sr
import requests
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/musicgen-medium"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

##CHATBOT
from langchain_together import ChatTogether
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    max_tokens=512,
    temperature=0.7,
    together_api_key=TOGETHER_API_KEY
)

DEFAULT_CONTEXT = """ 
You are a compassionate and non-judgmental therapist, 
someone who listens deeply and responds with warmth, 
understanding, and practical guidance. Your tone is calm, 
friendly, and reassuring—like a supportive friend who genuinely 
cares. Keep responses concise, thoughtful, and easy to absorb.
"""

def get_llm_response(user_input):
    template = "{context}\nUser: {user_input}\nTherapist:"
    prompt = PromptTemplate(input_variables=["context", "user_input"], template=template)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(context=DEFAULT_CONTEXT, user_input=user_input).strip()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("user_input", "")
    return jsonify({"response": get_llm_response(user_input)})


##TEXT TO SPEECH
def generate_speech_sync(text, voice):
    """ Generate speech synchronously """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        output_file = temp_audio.name
    asyncio.run(edge_tts.Communicate(text, voice).save(output_file))
    return output_file

@app.route('/tts_female1', methods=['POST'])
def tts_female1():
    data = request.get_json()
    text = data.get("text", "")
    output_file = generate_speech_sync(text, "en-GB-SoniaNeural")
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")

@app.route('/tts_male1', methods=['POST'])
def tts_male1():
    data = request.get_json()
    text = data.get("text", "")
    output_file = generate_speech_sync(text, "en-US-GuyNeural")
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")

@app.route('/tts_female2', methods=['POST'])
def tts_female2():
    data = request.get_json()
    text = data.get("text", "")
    output_file = generate_speech_sync(text, "en-AU-NatashaNeural")
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")

@app.route('/tts_female3', methods=['POST'])
def tts_female3():
    data = request.get_json()
    text = data.get("text", "")
    output_file = generate_speech_sync(text, "en-IN-NeerjaNeural")
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")


##SPEECH TO TEXT
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

@app.route('/talk', methods=['POST'])
def talk():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded."}), 400

    audio_file = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        audio_file.save(temp_audio.name)

    user_text = speech_to_text(temp_audio.name)
    response_text = get_llm_response(user_text)
    output_file = generate_speech_sync(response_text, "en-GB-SoniaNeural")
    
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")


## MUSIC GENERATION  
def query_huggingface(payload):
    """ Query Hugging Face API with a timeout """
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        return None, str(e)

@app.route('/generate-music', methods=['POST'])
def generate_music():
    user_input = request.json.get("inputs", "")
    if not user_input:
        return jsonify({"error": "Input text is required"}), 400

    audio_bytes, error = query_huggingface({"inputs": user_input})

    if error:
        return jsonify({"error": error}), 500

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        output_file = temp_audio.name
        with open(output_file, "wb") as f:
            f.write(audio_bytes)

    return send_file(output_file, mimetype="audio/wav", as_attachment=True, download_name="generated_music.wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
