from web_chat.llm.qwen import default_qwen_turbo, default_qwen_max


messages = [
]

while True:
    user_input = input("User: ")
    if user_input.strip() == "exit":
        break
    messages.append({"role": "user", "content": user_input})
    response: str = default_qwen_max.chat(messages = messages, raw_response = False, enable_search = True)
    print("Qwen: " + response)
    messages.append({"role": "assistant", "content": response})