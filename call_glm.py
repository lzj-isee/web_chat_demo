from web_chat.llm.glm import default_glm_3_turbo, default_glm_4_turbo


messages = [
]

while True:
    user_input = input("User: ")
    if user_input.strip() == "exit":
        break
    messages.append({"role": "user", "content": user_input})
    # response: str = default_glm_3_turbo.chat(messages = messages, raw_response = False)
    response: str = default_glm_4_turbo.chat(messages = messages, raw_response = False, tools = [{"type": "web_search", "web_search": {"enable": True}}])
    print("GLM: " + str(response))
    messages.append({"role": "assistant", "content": response})