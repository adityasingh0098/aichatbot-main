import ollama

messages = []

print("🤖 AI Chatbot")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye! 👋")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    bot_reply = response["message"]["content"]

    print("Bot:", bot_reply)

    messages.append({
        "role": "assistant",
        "content": bot_reply
    })