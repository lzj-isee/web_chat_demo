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
            "content": "战舰世界Z44的鱼类射速是多少"
        }, {
            "role": "assistant", 
            "content": "战舰世界中的Z44驱逐舰的鱼雷射速是0.71发/分钟¹。这意味着它的鱼雷装填时间是85秒¹。这是在没有任何技能或装备加成的情况下的数据。如果有相关的技能或装备加成，这个射速会有所提高。例如，如果使用了鱼雷装填系统改动1这个装备，鱼雷装填时间可以减少到65秒²。这样，Z44的鱼雷射速就会相应地提高。希望这个信息对你有所帮助！"
        }, {
            "role": "user", 
            "content": "“如果使用了鱼雷装填改动1这个装备，鱼类装填时间可以减少到65秒”，你还要考虑到激素这个技能的作用，如何考虑舰长技能，装填最快能有多少"
        }
    ]
    response = rewrite_robot.infer(messages = messages)
    print(response)
