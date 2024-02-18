from web_chat.llm.basic import _LLM
from web_chat import tools

class ServerRobot(object):
    def __init__(self, llm: _LLM) -> None:
        self.llm = llm

    def _generate_input_messages(self, chat_history: list[dict], citations: list[str]) -> list[dict]:
        if chat_history[0]["role"] == "system":
            chat_history = chat_history[1:]

        question = chat_history[-1]["content"]
        chat_history = chat_history[:-1]

        context = "\n\n".join(
            [
                f"[citation:{i}]: {citation}" for i, citation in enumerate(citations)
            ]
        )

        messages = [
            {
                "role": "system", 
                "content": f"Today's date is {tools.get_current_datetime()}. You are a smart AI assistant. You are given a user question, and please write clean, concise and accurate answer to the question.\n\nYou will be given a set of related contexts to the question, each starting with a reference number like [citation:x], where x is a number. Please use the context and cite the context at the end of each sentence in the format [citation:x] if applicable. If a sentence comes from multiple contexts, please list all applicable citations, like [citation:3][citation:5]."
            }
        ]
        messages += chat_history
        messages += [
            {
                "role": "user", 
                "content": f"Here are the contexts: \n\n{context}\n\nAnd answer the following question:\n{question}"
            }
        ]
        return messages
    
    def infer(self, chat_history: list[dict], citations: list[str]) -> str:
        llm_content = self.llm.chat(
            messages = self._generate_input_messages(
                chat_history = chat_history, 
                citations = citations
            ), 
            raw_response = False
        )
        return llm_content
    
    async def async_infer(self, chat_history: list[dict], citations: list[str]) -> str:
        llm_content = await self.llm.async_chat(
            messages = self._generate_input_messages(
                chat_history = chat_history, 
                citations = citations
            ), 
            raw_response = False
        )
        return llm_content