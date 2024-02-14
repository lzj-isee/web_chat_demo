from abc import ABC, abstractmethod


class _LLM(ABC):

    @abstractmethod
    def chat(self, messages: list[dict], raw_response: bool = False, **kwargs) -> str | dict:
        pass

    @abstractmethod
    async def async_chat(self, messages: list[dict], raw_response: bool = False, **kwargs) -> str | dict:
        pass