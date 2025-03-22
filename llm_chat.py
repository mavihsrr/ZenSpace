from flask import Flask, request, jsonify, send_file
import os
import edge_tts
import asyncio
import tempfile
from dotenv import load_dotenv
from langchain_together import ChatTogether
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


load_dotenv()

app = Flask(__name__)

VOICE = "en-GB-SoniaNeural"

llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    max_tokens=512,
    temperature=0.7,
    together_api_key=os.getenv("TOGETHER_API_KEY")
)

DEFAULT_CONTEXT = "You are a helpful, empathetic therapist. Respond with care and insight to the user's concerns."

def get_llm_response(user_input, context):
    template = "{context}\nUser: {user_input}\nTherapist:"
    prompt = PromptTemplate(input_variables=["context", "user_input"], template=template)
    
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(context=context, user_input=user_input)
    
    return response.strip()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("user_input", "")
    context = """
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
    response_text = get_llm_response(user_input, context)
    return jsonify({"response": response_text})

@app.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get("text", "")
    
    output_file = tempfile.gettempdir() + "/response.mp3"
    asyncio.run(edge_tts.Communicate(text, VOICE).save(output_file))
    
    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True, download_name="response.mp3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) 
