from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# ENV VARIABLE
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# OPENROUTER CLIENT
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# LOAD COMPANY DATA
with open("company_data.txt", "r", encoding="utf-8") as file:
    company_context = file.read()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        user_message = data.get("message")

        # CONTEXT PROMPT
        system_prompt = f"""
You are the official AI assistant of the company.

Answer ONLY based on the company information below.

If information is unavailable, politely say:
"I currently don't have that information."

COMPANY INFORMATION:
{company_context}
"""

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=300
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
