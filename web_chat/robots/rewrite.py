from web_chat.llm.basic import _LLM
from web_chat.definition.prompts import get_rewrite_prompt

class RewriteRobot(object):
    def __init__(self, llm: _LLM) -> None:
        self.llm = llm

    def _generate_input_messages(self, chat_history: list[dict]) -> list[dict]:
        prompts = get_rewrite_prompt()

        if chat_history[0]["role"] == "system":
            chat_history = chat_history[1:]
        _chat_history = "\n".join([
            f"User: {item['content']}" if item["role"] == "user" else f"You: {item['content']}"  for item in chat_history
        ])
        prompts[-1]["content"] = prompts[-1]["content"].format(chat_history = _chat_history)
        return prompts
    
    def infer(self, messages: list[dict]) -> str:
        llm_content = self.llm.chat(
            messages = self._generate_input_messages(chat_history = messages), 
            raw_response = False
        )
        return llm_content
    
    async def async_infer(self, messages: list[dict]) -> str:
        llm_content = await self.llm.async_chat(
            messages = self._generate_input_messages(chat_history = messages), 
            raw_response = False
        )
        return llm_content
    

if __name__ == "__main__":
    from web_chat.llm.glm import default_glm_3_turbo
    rewrite_robot = RewriteRobot(llm = default_glm_3_turbo)
    messages = [
        {
            "role": "user", 
            "content": "我在一台电脑push了一个github项目，现在我换电脑了，能正常pull，改了一些东西，怎么再push？"
        }
    ]
    response = rewrite_robot.infer(messages = messages)
    print(response)
