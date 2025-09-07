from flask import Flask, render_template, request, jsonify
from jarvis_logic import handle_query

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("message", "")
    response = handle_query(query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
