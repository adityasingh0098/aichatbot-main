from flask import Flask, render_template, request, jsonify
import ollama
import json
import os
import threading
import webview

app = Flask(__name__)

messages = []
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)["memories"]
    return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump({"memories": memory}, file, indent=4)

memory = load_memory()

@app.route("/",methods=["GET","POST"])
def home():
    return render_template("index.html",messages=messages)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]

    messages.append({
        "role": "user",
        "content": user_message
    })
    if user_message.lower().startswith("remember "):
        fact = user_message[9:].strip()
        memory.append(fact)
        save_memory(memory)

    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    bot_reply = response["message"]["content"]

    messages.append({
        "role": "assistant",
        "content": bot_reply
    })
    return render_template("index.html", messages=messages)
    
@app.route("/clear")
def clear():
    messages.clear()
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=5000, debug=False),
        daemon=True
    ).start()

    webview.create_window(
        "My Chatbot",
        "http://127.0.0.1:5000",
        width=1000,
        height=700
    )

    webview.start()