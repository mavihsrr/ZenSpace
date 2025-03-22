# from flask import Flask, request, jsonify
# import requests
# from IPython.display import Audio
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)

# API_URL = "https://router.huggingface.co/hf-inference/models/facebook/musicgen-medium"
# headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     if response.status_code == 200:
#         return response.content
#     else:
#         raise Exception(f"Error: {response.status_code}, {response.text}")

# @app.route('/generate-music', methods=['POST'])
# def generate_music():
#     # Get user input from the request
#     user_input = request.json.get("inputs", "")
#     if not user_input:
#         return jsonify({"error": "Input text is required"}), 400

#     try:
#         # Query the Hugging Face API
#         audio_bytes = query({"inputs": user_input})

#         # Save the audio file
#         output_file = "generated_music.wav"
#         with open(output_file, "wb") as f:
#             f.write(audio_bytes)

#         # Return success response
#         return jsonify({
#             "message": "Music generated successfully",
#             "file_path": os.path.abspath(output_file)
#         }), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)