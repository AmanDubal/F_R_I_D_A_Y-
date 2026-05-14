from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

AI_URL = "https://aicallingagent-production-b135.up.railway.app/chat"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():

    try:

        data = request.get_json()

        print("DATA :", data)

        user_message = data.get('message')

        print("USER :", user_message)

        response = requests.post(
            AI_URL,
            json={
                "prompt": user_message
            },
            timeout=120
        )

        print("STATUS :", response.status_code)

        print("RAW :", response.text)

        ai_data = response.json()

        ai_response = ai_data.get('response', str(ai_data))

        print("AI :", ai_response)

        return jsonify({
            "response": ai_response
        })

    except Exception as e:

        print("ERROR :", e)

        return jsonify({
            "response": f"Server Error : {e}"
        })if __name__ == '__main__':
    app.run(debug=True)
