# chatbot_server.py
from flask import Flask, request, jsonify
from lib.ecommerce_agent import agent
from flask_cors import CORS
from flask import send_from_directory


app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})  # Enable CORS for /chat


@app.route("/")
def index():
    return send_from_directory("static", "config.html")  # option

@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

@app.route("/demo")
def demo():
    return send_from_directory("static", "demo.html")  # option

@app.route("/chat", methods=["POST", "OPTIONS"])  # Handle preflight
def chat():
    if request.method == "OPTIONS":
        return '', 200
    user_input = request.json.get("query", "")
    prompt = f""" Answer the question using the knowledge base.
    - Use bullet points and formatting.
    - Focus on clarity and helpfulness.
    Question: {user_input}
    """
    
    print(f"Received query: {user_input}")
    
    response = agent.run(prompt)
    return jsonify({"response": response.content})  # grab cont

if __name__ == "__main__":
    app.run(port=5050)
