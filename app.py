from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Your custom LLM URL
CUSTOM_LLM_URL = os.getenv("CUSTOM_LLM_URL")

@app.route("/")
def home():
    return {
        "status": "running",
        "message": "Custom LLM Proxy Running"
    }

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json

        response = requests.post(
            CUSTOM_LLM_URL,
            json=data,
            headers={
                "Content-Type": "application/json"
            }
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)