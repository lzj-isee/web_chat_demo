from web_chat import tools

def get_intent_prompt() -> list[dict]:
    examples = [
        {
            "role": "system", 
            "content": f"You are chatting with a user. You can use Google search to form a response. What do you type in the search box? Today's date is {tools.get_current_datetime()}"
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: Who made you?", 
                "[Search needed?"
            ])
        }, {
            "role": "assistant", 
            "content": "No."
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: 帮我用python写个蓄水池抽样代码", 
                "[Search needed?"
            ])
        }, {
            "role": "assistant", 
            "content": "No."
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: 韦伯天文望远镜最近有什么发现", 
                "[Search needed?"
            ])
        }, {
            "role": "assistant", 
            "content": "Yes."
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: llamaindex这个github项目有多少star", 
                "You: LlamaIndex项目在GitHub上有28k颗星星。这是一个数据框架，用于构建您的LLM应用。希望这个信息对您有所帮助！", 
                "User: 和langchain这个项目比谁的星星多", 
                "[Search needed?"
            ])
        }, {
            "role": "assistant", 
            "content": "Yes."
        }, {
            "role": "user", 
            "content": "\n".join([
                "User：do you know yoko ono?", 
                "[Search needed?"
            ])
        }, {
            "role": "assistant", 
            "content": "Yes."
        }
    ]
    placehold = {
        "role": "user",
        "content": "{chat_history}\n[Search needed?"
    }
    return examples + [placehold]

def get_rewrite_prompt() -> list[dict]:
    prefix = "\nRewrite all the chat history to make it a self-contained question"
    examples = [
        {
            "role": "system", 
            "content": f"You are chatting with a user. Rewrite the user's last question in conjunction with all chat history to make it a self-contained question. Use Google search to form a response. What do you type in the search box? Today's date is {tools.get_current_datetime()}"
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: 你看到布洛克-珀迪去年是如何被选入国家橄榄球联盟的吗？", 
                prefix
            ])
        }, {
            "role": "assistant", 
            "content": "Brock Purdy 是如何在 2022 年被选入国家橄榄球联盟的？"
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: do you know yoko ono?", 
                "You: Yes, I know who Yoko Ono is. She is a Japanese American musician who has released 14 studio albums and won a Grammy Award. She is also the 11th most successful dance club artist of all time, according to Billboard Magazine. Ono is best known for her work with the Plastic Ono Band and for her album Starpeace.", 
                "User: was she related to the beatles?", 
                "You: Yes, she was married to John Lennon of the Beatles.", 
                "User: really? why do people hate her so much?", 
                prefix
            ])
        }, {
            "role": "assistant", 
            "content": "reasons people dislike Yoko Ono"
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: llamaindex这个github项目有多少star", 
                "You: LlamaIndex项目在GitHub上有28k颗星星。这是一个数据框架，用于构建您的LLM应用。希望这个信息对您有所帮助！", 
                "User: 和langchain这个项目比谁的星星多", 
                prefix
            ])
        }, {
            "role": "assistant", 
            "content": "LlamaIndex和LangChain的相比谁的Github Star数量更多"
        }
    ]
    placehold = {
        "role": "user", 
        "content": "{chat_history}\n" + prefix
    }
    return examples + [placehold]

def get_search_prompt_full() -> list[dict]:
    prefix = "\nRewrite all the chat history into queries for Google search: "
    examples = [
        {
            "role": "system", 
            "content": f"You are chatting with a user. Enumerate Google search query statements combined with all chat history. Today's date is {tools.get_current_datetime()}"
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: do you know yoko ono?", 
                prefix
            ])
        }, {
            "role": "assistant", 
            "content": "* who is yoko ono?"
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: llamaindex这个github项目有多少star", 
                "You: LlamaIndex项目在GitHub上有28k颗星星。这是一个数据框架，用于构建您的LLM应用。希望这个信息对您有所帮助！", 
                "User: 和langchain这个项目比谁的星星多", 
                prefix
            ])
        }, {
            "role": "assistant", 
            "content": "\n".join([
                "* LlamaIndex Github Star", 
                "* LangChain Github Star"
            ])
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: Tell me about Murakami.", 
                "You: Murakami is a Japanese author. He is best known for his novels Norwegian Wood, The Wind-Up Bird Chronicle, Kafka on the Shore, and 1Q84."
                "User: I meant the baseball player.", 
                prefix
            ])
        }, {
            "role": "assistant", 
            "content": "\n".join([
                "* who is Murakami the baseball player?"
            ])
        }, {
            "role": "user", 
            "content": "\n".join([
                "User: 坚果和大米哪个热量高", 
                prefix
            ])
        }, {
            "role": "assistant", 
            "content": "\n".join([
                "* 坚果热量", 
                "* 大米热量"
            ])
        }
    ]
    placeholder = {
        "role": "user", 
        "content": "{chat_history}\n" + prefix
    }
    return examples + [placeholder]

def get_search_prompt_part() -> list[dict]:
    pass