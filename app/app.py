from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS

RASA_URL = 'http://localhost:5005/webhooks/rest/webhook'

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Send message to Rasa
    response = requests.post(RASA_URL, json={'message': user_message})
    rasa_responses = response.json()

    return jsonify(rasa_responses)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
