from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Hugging Face Router client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message")
    try:
        completion = client.chat.completions.create(
            model="google/flan-t5-base",  # <-- free model
            messages=[{"role": "user", "content": user_input}],
            max_tokens=300
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"AI Error: {e}"

    return jsonify({"reply": reply})