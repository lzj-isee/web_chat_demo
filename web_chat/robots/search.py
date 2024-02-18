from web_chat.llm.basic import _LLM
from web_chat.definition.prompts import get_search_prompt_full

class SearchRobot(object):
    def __init__(self, llm: _LLM) -> None:
        self.llm = llm

    def _generate_input_messages(self, chat_history: list[dict]) -> list[dict]:
        prompts = get_search_prompt_full()

        if chat_history[0]["role"] == "system":
            chat_history = chat_history[1:]
        _chat_history = "\n".join([
            f"User: {item['content']}" if item["role"] == "user" else f"You: {item['content']}"  for item in chat_history
        ])
        prompts[-1]["content"] = prompts[-1]["content"].format(chat_history = _chat_history)
        return prompts
    
    def _wrap_llm_response(self, content: str) -> list[str]:
        lines = content.split("\n")
        results = [
            line.lstrip("* ") for line in lines if line.startswith("* ")
        ]
        return results
    
    def infer(self, messages: list[dict]) -> list[str]:
        llm_content = self.llm.chat(
            messages = self._generate_input_messages(chat_history = messages), 
            raw_response = False
        )
        return self._wrap_llm_response(content = llm_content)

    async def async_infer(self, messages: list[dict]) -> list[str]:
        llm_content = await self.llm.async_chat(
            messages = self._generate_input_messages(chat_history = messages), 
            raw_response = False
        )
        return self._wrap_llm_response(content = llm_content)
    

if __name__ == "__main__":
    from web_chat.llm.glm import default_glm_3_turbo
    rewrite_robot = SearchRobot(llm = default_glm_3_turbo)
    messages = [
        {
            "role": "user", 
            "content": "帮我搜下最近关于EA的新闻"
        }
    ]
    response = rewrite_robot.infer(messages = messages)
    print(response)