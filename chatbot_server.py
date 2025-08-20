# chatbot_server.py
from flask import Flask, request, jsonify
from lib.agents import agent, validation_agent
from lib.chat_logger import ChatLogger
from flask_cors import CORS
from flask import send_from_directory
import os



app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})  # Enable CORS for /chat

# Initialize the chat logger
chat_logger = ChatLogger()


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

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return '', 200
    
    data = request.json
    user_input = data.get("query", "")
    user_id = data.get("user_id", "default_user")
    session_id = data.get("session_id")
        
    print(f"Received query: {user_input}")
    
    max_attempts = 2
    attempt = 0
    original_query = user_input  # Store original query
    
    while attempt < max_attempts:
        attempt += 1
        print(f"Attempt {attempt}/{max_attempts}")
        
        # Get response from main agent
        response = agent.run(
            user_input, 
            user_id=user_id,
            session_id=session_id
        )
        
        print(f"Main agent response length: {len(response.content)}")
        
        # Validate the response
        validation_prompt = f"""
        Validate this customer service response:
        
        USER QUERY: "{original_query}"
        AGENT RESPONSE: "{response.content}"
        
        Check for:
        1. Relevance to user's question
        2. Completeness of answer
        3. Proper formatting (product cards, clarification questions)
        4. Accuracy from knowledge base
        
        Respond with either:
        - "APPROVED" if the response is good
        - "REJECTED: [specific issues]" if there are problems
        """
        
        validation_result = validation_agent.run(validation_prompt)
        print(f"Full validation result: {validation_result.content}")
        
        # Extract the actual validation decision from reasoning output
        validation_content = validation_result.content.lower()
        
        # Check if response contains approval or rejection
        if "approved" in validation_content or "good" in validation_content:
            print("✅ Response approved by validation agent")
            
            # Log the chat interaction
            chat_logger.log_chat(
                user_id=user_id,
                question=original_query,
                answer=response.content,
                session_id=agent.session_id,
                validation_status="approved",
                attempts=attempt
            )
            
            return jsonify({
                "response": response.content,
                "session_id": agent.session_id,
                "validation_status": "approved",
                "attempts": attempt
            })
        
        elif "rejected" in validation_content or "issues" in validation_content or "problems" in validation_content:
            print(f"❌ Response rejected on attempt {attempt}")
            
            if attempt < max_attempts:
                # Create regeneration prompt with feedback
                regeneration_prompt = f"""
                The user asked: "{original_query}"
                
                My previous response had quality issues. Please provide a better response that:
                - Directly addresses the user's question
                - Follows proper formatting guidelines
                - Asks clarifying questions if needed
                - Uses knowledge base information accurately
                
                Original user query: {original_query}
                """
                
                print("🔄 Regenerating response with improvements...")
                user_input = regeneration_prompt
                continue
            else:
                print("⚠️ Max attempts reached, returning last response")
                
                # Log the chat interaction with rejected status
                chat_logger.log_chat(
                    user_id=user_id,
                    question=original_query,
                    answer=response.content,
                    session_id=agent.session_id,
                    validation_status="rejected_max_attempts",
                    attempts=attempt
                )
                
                return jsonify({
                    "response": response.content,
                    "session_id": agent.session_id,
                    "validation_status": "rejected_max_attempts",
                    "attempts": attempt,
                    "validation_feedback": validation_result.content
                })
        else:
            # If validation result is unclear, approve by default
            print("⚠️ Unclear validation result, approving by default")
            
            # Log the chat interaction with approved_default status
            chat_logger.log_chat(
                user_id=user_id,
                question=original_query,
                answer=response.content,
                session_id=agent.session_id,
                validation_status="approved_default",
                attempts=attempt
            )
            
            return jsonify({
                "response": response.content,
                "session_id": agent.session_id,
                "validation_status": "approved_default",
                "attempts": attempt
            })
    
    # Fallback
    # Log the chat interaction with fallback status
    chat_logger.log_chat(
        user_id=user_id,
        question=original_query,
        answer=response.content,
        session_id=agent.session_id,
        validation_status="fallback",
        attempts=attempt
    )
    
    return jsonify({
        "response": response.content,
        "session_id": agent.session_id,
        "validation_status": "fallback",
        "attempts": attempt
    })

@app.route("/chat-history", methods=["GET"])
def get_chat_history():
    """Get chat history for a user or session"""
    user_id = request.args.get("user_id")
    session_id = request.args.get("session_id")
    limit = request.args.get("limit", 10, type=int)
    
    if session_id:
        history = chat_logger.get_session_chat_history(session_id, limit)
        return jsonify({"session_id": session_id, "history": history})
    elif user_id:
        history = chat_logger.get_user_chat_history(user_id, limit)
        return jsonify({"user_id": user_id, "history": history})
    else:
        return jsonify({"error": "Either user_id or session_id must be provided"}), 400

if __name__ == "__main__":
    # app.run(port=5050) # Use this for local testing
    port = int(os.environ.get("PORT", 5000))  # use PORT from environment or fallback to 5000
    app.run(host="0.0.0.0", port=port)
 