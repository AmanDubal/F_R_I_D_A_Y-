from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# GET API KEY FROM ENVIRONMENT
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# CHECK IF API KEY EXISTS
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing!")

# CREATE CLIENT
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message")

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=150
        )

        ai_response = response.choices[0].message.content

        return jsonify({
            "response": ai_response
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
