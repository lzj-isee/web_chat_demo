from web_chat.llm.qwen import default_qwen_turbo


messages = [
    {
        "role": "user", 
        "content": "你好"
    }
]

response: str = default_qwen_turbo.chat(messages = messages, raw_response = False)

print(response)