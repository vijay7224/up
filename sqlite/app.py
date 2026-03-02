from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI

app = Flask(__name__)

# Hugging Face Router client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message")
    try:
        # User-friendly prompt instructs the model to give short, clear, beginner-friendly answers
        system_prompt = (
            "You are a friendly AI assistant. Respond in simple, concise, and approachable language. "
            "Do NOT include internal thoughts, <think> tags, or reasoning steps. "
            "Use short sentences, emojis if appropriate, and examples for clarity."
        )
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",  # free chat-compatible model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"AI Error: {e}"
    return jsonify({"reply": reply})

