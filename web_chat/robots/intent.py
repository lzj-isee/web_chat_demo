from web_chat.llm.basic import _LLM
from web_chat.definition.dataframe import (
    QueryIntent
)
from web_chat.definition.prompts import get_intent_prompt

class IntentRobot(object):
    
    def __init__(self, llm: _LLM) -> None:
        self.llm = llm

    def _generate_input_messages(self, chat_history: list[dict]) -> list[dict]:
        prompts = get_intent_prompt()

        if chat_history[0]["role"] == "system":
            chat_history = chat_history[1:]
        _chat_history = "\n".join([
            f"User: {item['content']}" if item["role"] == "user" else f"You: {item['content']}"  for item in chat_history
        ])
        prompts[-1]["content"] = prompts[-1]["content"].format(chat_history = _chat_history)
        return prompts
    
    def _wrap_llm_response(self, content: str) -> QueryIntent:
        if content.lower().startswith("yes"):
            return QueryIntent.WEB
        elif content.lower().startswith("no"):
            return QueryIntent.CHAT
        else:
            return QueryIntent.UNK
        
    def infer(self, messages: list[dict]) -> QueryIntent:
        llm_content = self.llm.chat(
            messages = self._generate_input_messages(chat_history = messages), 
            raw_response = False
        )
        return self._wrap_llm_response(content = llm_content)

    async def async_infer(self, messages: list[dict]) -> QueryIntent:
        llm_content = await self.llm.async_chat(
            messages = self._generate_input_messages(chat_history = messages), 
            raw_response = False
        )
        return self._wrap_llm_response(content = llm_content)
    

if __name__ == "__main__":
    from web_chat.llm.glm import default_glm_3_turbo
    intent_analyzer = IntentRobot(llm = default_glm_3_turbo)
    messages = [
        {
            "role": "user", 
            "content": "帮我翻译下这句话成英文：“你是一个机器人，正在与用户对话，你可以使用谷歌搜索”"
        }
    ]
    response = intent_analyzer.infer(messages = messages)
    print(response)