from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# ✅ Init App
app = Flask(__name__)
CORS(app)

# ✅ Set API Key from env
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ GPT Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["user_input"]

        # ✅ Gunakan client.chat.completions.create (v1 API)
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are TAS.DAR Coach AI. Respond reflectively and clearly."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Port dinamik Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
