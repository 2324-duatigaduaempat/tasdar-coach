
from flask import Flask, request, jsonify
from pymongo import MongoClient
import openai
import os

app = Flask(__name__)

# MongoDB setup
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["tasdar_ai"]
core = db["identity_core"]

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_system_prompt():
    doc = core.find_one({"id": "tasdar_v1.0"})
    return doc["system_prompt"]["prompt"]

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    system_prompt = get_system_prompt()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})
