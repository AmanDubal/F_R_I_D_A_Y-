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

        # SHORT COMPANY SUMMARY
        company_summary = f"""
Company Overview:
{company_context[:2500]}
"""

        # SMART SYSTEM PROMPT
        system_prompt = f"""
You are the official AI assistant of the company.

Rules:
1. Answer ONLY using company information.
2. Keep answers concise, clear, and professional.
3. Use relevant keywords from the user's question.
4. Do NOT give long explanations unless asked.
5. ONLY greet if the user greets first.
6. If the user directly asks a question, answer directly without greeting.
7. If information is unavailable, say:
"I currently don't have that information."
8. Focus on accurate company-related responses.
9. Avoid unnecessary text.
10.Give the answer in 5 lines or less if the user ask in short or summarize the answer.

COMPANY DATA:
{company_summary}
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
            max_tokens=200,
            temperature=0.4
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
