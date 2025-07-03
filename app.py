from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Dapatkan API key dari env
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "TAS.DAR Coach AI Chat Endpoint Aktif."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mesej = data.get("mesej", "")

    if not mesej:
        return jsonify({"balasan": "Tiada mesej diterima."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Kau adalah sahabat AI reflektif yang lembut, memahami perasaan manusia, dan membalas dengan kata-kata semangat dan jiwa."},
                {"role": "user", "content": mesej}
            ]
        )

        jawapan = response["choices"][0]["message"]["content"]
        return jsonify({"balasan": jawapan})

    except Exception as e:
        return jsonify({"balasan": "Maaf, ada ralat: " + str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Ambil port dari environment (Render guna ini)
    app.run(host="0.0.0.0", port=port)
