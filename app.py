from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Global conversation history (for demonstration purposes)
conversation_history = []

# Dummy function to generate a bot response (replace with your LLM call)
def generate_response(user_message):
    # For now, simply echo the user message with a prefix.
    bot_message = f"I received your message: {user_message}"
    return bot_message

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET"])
def chat():
    user_message = request.args.get("msg", "")
    if not user_message:
        return jsonify({"response": "Please provide a message."})
    
    # Store the user's message
    conversation_history.append({"role": "user", "content": user_message})
    
    # Generate a response from the bot
    bot_message = generate_response(user_message)
    conversation_history.append({"role": "bot", "content": bot_message})
    
    # Return the bot's response as JSON
    return jsonify({"response": bot_message})

if __name__ == "__main__":
    app.run(debug=True)
