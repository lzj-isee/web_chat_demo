from web_chat.llm.basic import _LLM
from web_chat import tools
from web_chat.definition.dataframe import RetrievalResult

class WorkerRobot(object):
    def __init__(self, llm: _LLM) -> None:
        self.llm = llm

    def _generate_input_messages(self, retrieval_result: RetrievalResult, query: str) -> list[dict]:
        system_content = f"You Google the user question and then extract the relevant parts of the article you find. Today's date is {tools.get_current_datetime()}. Do not give any information that is not related to the question, and do not repeat. Just say 'NOTHING' if the given context do not provide sufficient information."
        messages = [
            {
                "role": "system", 
                "content": system_content
            }, {
                "role": "user", 
                "content": f"You find the following context: \n\nTitle: {retrieval_result.title}\n\nContent:\n{retrieval_result.content}\n\nPlease find the part of the context that is relevant to the following search question:\n{query}\n\nYour answer must be in the same language as the original question."
            }
        ]
        return messages
    
    def _parse_llm_response(self, content: str) -> str | None:
        if content.upper().startswith("NOTHING"):
            return None
        return content
    
    def infer(self, query: str, retrieval_result: RetrievalResult) -> str | None:
        llm_content = self.llm.chat(
            messages = self._generate_input_messages(
                retrieval_result = retrieval_result, 
                query = query
            ), 
            raw_response = False
        )
        return self._parse_llm_response(content = llm_content)
    
    async def async_infer(self, query: str, retrieval_result: RetrievalResult) -> str | None:
        llm_content = await self.llm.async_chat(
            messages = self._generate_input_messages(
                retrieval_result = retrieval_result, 
                query = query
            ), 
            raw_response = False
        )
        return self._parse_llm_response(content = llm_content)