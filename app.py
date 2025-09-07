import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import jarvis_logic

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    assistant_reply = jarvis_logic.get_response(user_message)
    return jsonify({'response': assistant_reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
