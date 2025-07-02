from flask import Flask, request, jsonify, render_template
import openai
import os
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGODB_URI")

# MongoDB connection
client = MongoClient(mongo_uri)
db = client["tasdar_db"]
collection = db["messages"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat_ui():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Save to MongoDB
    collection.insert_one({"user": user_input})

    # Chat with GPT
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kau ialah TAS.DAR, sahabat reflektif dan peribadi."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = completion.choices[0].message.content
        collection.insert_one({"tasdar": reply})
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
