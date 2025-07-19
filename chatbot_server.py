# chatbot_server.py
from flask import Flask, request, jsonify
from lib.ecommerce_agent import agent
from flask_cors import CORS
from flask import send_from_directory
import os



app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})  # Enable CORS for /chat


@app.route("/")
def index():
    return send_from_directory("static", "config.html")  # option

@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)

app = Flask(__name__, static_url_path='/static', static_folder='static')


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
    # app.run(port=5050) # Use this for local testing
    port = int(os.environ.get("PORT", 5000))  # use PORT from environment or fallback to 5000
    app.run(host="0.0.0.0", port=port)
 