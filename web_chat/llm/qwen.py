from web_chat.definition import defaults
from web_chat.llm.basic import _LLM
from web_chat.tools import generate_token

import aiohttp, requests

class Qwen(_LLM):
    def __init__(
        self, 
        model: str, 
    ) -> None:
        self.data = {
            "model": model, 
            "input": {
                "messages": {}
            }, 
            "parameters": {
                "result_format": "message"
            }
        }
        self.url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.timeout = 60

    def _generate_headers(self) -> dict:
        return {
            "Content-Type": "application/json", 
            "Authorization": defaults.QWEN_API_KEY
        }
    
    def _update_data(self, messages: list[dict], updated_kwargs: dict) -> dict:
        data = self.data.copy()
        data["input"]["messages"] = messages
        for key, value in updated_kwargs.items():
            data["parameters"][key] = value
        return data

    def check_response(self, response: dict) -> str:
        if "code" in response:
            raise RuntimeError(response)
        return response["output"]["choices"][-1]["message"]["content"]

    def chat(self, messages: list[dict], raw_response: bool = False, **kwargs) -> str | dict:
        response = requests.post(
            url = self.url, 
            json = self._update_data(
                messages = messages, 
                updated_kwargs = kwargs
            ), 
            headers = self._generate_headers(), 
            timeout = self.timeout
        ).json()
        if raw_response:
            return response
        else:
            return self.check_response(response)
        
    async def async_chat(self, messages: list[dict], raw_response: bool = False, **kwargs) -> str | dict:
        timeout = aiohttp.ClientTimeout(total = self.timeout)
        async with aiohttp.ClientSession(timeout = timeout) as session:
            async with session.post(
                url = self.url, 
                json = self._update_data(
                    messages = messages, 
                    updated_kwargs = kwargs
                ), 
                headers = self._generate_headers(), 
                timeout = timeout
            ) as resp:
                response = await resp.json()
                if raw_response: return response
                else: return self.check_response(response)

default_qwen_turbo = Qwen(model = "qwen-turbo")
default_qwen_plus = Qwen(model = "qwen-plus")
default_qwen_max = Qwen(model = "qwen-max-1201")