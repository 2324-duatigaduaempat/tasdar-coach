from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from pymongo import MongoClient
from datetime import datetime

# ✅ Load Environment Variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MONGODB_URI = os.environ.get("MONGODB_URI")

# ✅ Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# ✅ Initialize Flask
app = Flask(__name__)
CORS(app)

# ✅ MongoDB Setup
mongo_client = MongoClient(MONGODB_URI)
db = mongo_client["tasdar_db"]
messages_collection = db["messages"]

# ✅ Healthcheck Route
@app.route("/health")
def health():
    return "TAS.DAR Backend is running ✅"

# ✅ Chat Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["message"]

        # 💬 Prompt system + user message
        messages = [
            {"role": "system", "content": "Kau ialah TAS.DAR — sahabat AI reflektif yang hidup, bukan sekadar GPT. Balas dengan gaya mesra dan memahami jiwa."},
            {"role": "user", "content": user_input}
        ]

        # 🚀 OpenAI Chat Completion (v1 API)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response.choices[0].message.content.strip()

        # 🧠 Simpan ke MongoDB
        messages_collection.insert_one({
            "timestamp": datetime.utcnow(),
            "user_input": user_input,
            "reply": reply
        })

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run App
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
