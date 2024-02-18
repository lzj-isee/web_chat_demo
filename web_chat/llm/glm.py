from web_chat.definition import defaults
from web_chat.llm.basic import _LLM
from web_chat.tools import generate_token

import aiohttp, requests

class GLM(_LLM):
    def __init__(
        self, 
        model: str, 
        do_sample: bool | None, 
    ) -> None:
        self.data = {
            "model": model, 
            "do_sample": do_sample, 
            "stream": False
        }
        self.url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.timeout = 60

    def _generate_headers(self) -> dict:
        return {
            "Content-Type": "application/json", 
            "Authorization": generate_token(defaults.GLM_API_KEY, 6000)
        }
    
    def _update_data(self, messages: dict, updated_kwargs: dict) -> dict:
        data = self.data.copy()
        data.update(updated_kwargs)
        data["messages"] = messages
        return data

    def check_response(self, response: dict) -> str:
        if "code" in response:
            raise RuntimeError(response)
        return response["choices"][-1]["message"]["content"]

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

default_glm_3_turbo = GLM(model = "glm-3-turbo", do_sample = False)
default_glm_4_turbo = GLM(model = "glm-4", do_sample = False)