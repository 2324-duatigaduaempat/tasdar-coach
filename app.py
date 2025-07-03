
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.json
    user_input = data.get("message", "")
    return {"reply": f"Balasan reflektif untuk: {user_input}"}

@app.route("/health")
def health():
    return "TAS.DAR Coach AI Chat Endpoint Aktif."
