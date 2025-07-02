from flask import Flask, request, jsonify, render_template
import os
import openai

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")  # Pastikan templates/index.html wujud

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)  # force = fallback kalau Content-Type tiada
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"response": response.choices[0].message["content"]})
    except Exception as e:
        print("OpenAI error:", e)
        return jsonify({"error": "Something went wrong"}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
