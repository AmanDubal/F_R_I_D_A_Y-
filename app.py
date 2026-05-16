import os
print("==> Starting imports...")

from flask import Flask, render_template, request, jsonify
print("==> Flask OK")

from flask_cors import CORS
print("==> CORS OK")

from openai import OpenAI
print("==> OpenAI OK")

app = Flask(__name__)
CORS(app)


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

MODEL = "gpt-4-turbo"

print("==> App initialized OK")


# ── Routes ─────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        print("DATA :", data)

        user_message = data.get('message', '')
        print("USER :", user_message)

        if not user_message:
            return jsonify({"response": "Please send a message."})

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=512
        )

        ai_response = response.choices[0].message.content
        print("AI :", ai_response)

        return jsonify({"response": ai_response})

    except Exception as e:
        print("ERROR :", e)
        return jsonify({"response": f"Server Error : {e}"})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
