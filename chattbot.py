from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = "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"


app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if not OPENROUTER_API_KEY:
        return jsonify({"error": "API key is missing"}), 500

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",  # Choose your preferred model
                "messages": [{"role": "user", "content": user_message}]
            }
        )

        response_data = response.json()

        print(response_data)

        # Extract chatbot response safely
        chatbot_reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response available.")
        

        return jsonify({"response": chatbot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
