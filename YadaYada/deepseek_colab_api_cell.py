# Colab cell: Flask API for DeepSeek
!pip install flask flask_cors pyngrok

from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok

app = Flask(__name__)
CORS(app)

def deepseek_chat(prompt):
    # TODO: Replace with your DeepSeek inference logic
    return "DeepSeek response to: " + prompt

@app.route('/deepseek-chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')
    response = deepseek_chat(prompt)
    return jsonify({'response': response})

public_url = ngrok.connect(5000)
print("DeepSeek API is live at:", public_url)

app.run(port=5000)
