from flask import Flask, request, jsonify
from jarvis_logic import handle_query

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_input = data.get("query", "")
    response = handle_query(user_input)
    return jsonify({"response": response})
if __name__ == "__main__":
    app.run(debug=True)

