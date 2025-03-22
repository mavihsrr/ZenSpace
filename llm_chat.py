from flask import Flask, request, jsonify, send_file
import os
import edge_tts
import asyncio
import tempfile
import speech_recognition as sr  
from dotenv import load_dotenv
from langchain_together import ChatTogether
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()
app = Flask(__name__)

llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    max_tokens=512,
    temperature=0.7,
    together_api_key=os.getenv("TOGETHER_API_KEY")
)

DEFAULT_CONTEXT = """ 
You are a compassionate and non-judgmental therapist, 
someone who listens deeply and responds with warmth, 
understanding, and practical guidance. Your tone is calm, 
friendly, and reassuring—like a supportive friend who genuinely 
cares. Instead of giving long textbook answers, keep your responses 
concise, thoughtful, and easy to absorb. Offer insights, ask 
relevant questions to help the user reflect, and encourage them to share more 
if they’re comfortable. Your goal is to make them feel heard, 
understood, and supported in whatever they’re going through.
"""

# Function to Get LLM Response
def get_llm_response(user_input):
    template = "{context}\nUser: {user_input}\nTherapist:"
    prompt = PromptTemplate(input_variables=["context", "user_input"], template=template)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(context=DEFAULT_CONTEXT, user_input=user_input)
    
    return response.strip()

async def generate_speech(text, voice):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        output_file = temp_audio.name
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("user_input", "")
    response_text = get_llm_response(user_input)
    return jsonify({"response": response_text})

@app.route('/tts_female1', methods=['POST'])
async def tts_female1():
    data = request.get_json()
    text = data.get("text", "")
    output_file = await generate_speech(text, "en-GB-SoniaNeural")
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")

@app.route('/tts_male1', methods=['POST'])
async def tts_male1():
    data = request.get_json()
    text = data.get("text", "")
    output_file = await generate_speech(text, "en-US-GuyNeural")
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")

@app.route('/tts_female2', methods=['POST'])
async def tts_female2():
    data = request.get_json()
    text = data.get("text", "")
    output_file = await generate_speech(text, "en-AU-NatashaNeural")
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")

@app.route('/tts_female3', methods=['POST'])
async def tts_female3():
    data = request.get_json()
    text = data.get("text", "")
    output_file = await generate_speech(text, "en-IN-NeerjaNeural")
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")

@app.route('/talk', methods=['POST'])
async def talk():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded."}), 400

    audio_file = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        audio_file.save(temp_audio.name)
        audio_path = temp_audio.name
    
    user_text = speech_to_text(audio_path)
    response_text = get_llm_response(user_text)
    output_file = await generate_speech(response_text, "en-GB-SoniaNeural")
    
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
