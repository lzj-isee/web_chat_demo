from web_chat.definition.dataframe import (
    RetrievalResult
)

from duckduckgo_search import DDGS, AsyncDDGS
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer

import os


class DuckDuckGo(object):
    def __init__(self, max_results: int = 5, region: str = "wt-wt") -> None:
        os.environ["http_proxy"] = "http://localhost:7890"
        os.environ["https_proxy"] = "http://localhost:7890"
        self.max_results = max_results
        self.region = region
        self.backend = "api"
        self.html2text = Html2TextTransformer()

    def _wrap_ddg_result(self, ddg_output: list[dict]) -> list[RetrievalResult]:
        urls = [_result["href"] for _result in ddg_output]
        docs = AsyncHtmlLoader(urls).load()
        docs_transformed = self.html2text.transform_documents(docs)
        finals = []
        for doc in docs_transformed:
            finals.append(
                RetrievalResult(
                    source_url = doc.metadata["source"], 
                    title  = doc.metadata.get("title", None), 
                    description = doc.metadata.get("description", None), 
                    content = doc.page_content
                )
            )
        return finals
    
    def retrieve(self, query: str) -> list[RetrievalResult]:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results = self.max_results, region = self.region, backend = self.backend)]
            return self._wrap_ddg_result(ddg_output = results)

    async def async_retrieve(self, query: str) -> list[RetrievalResult]:
        async with AsyncDDGS() as ddgs:
            results = [r async for r in ddgs.text(query, max_results = self.max_results, region = self.region, backend = self.backend)]
            return self._wrap_ddg_result(ddg_output = results)
        
if __name__ == "__main__":
    retriever = DuckDuckGo()
    results = retriever.retrieve(query = "战地2042 M5A3射速")
    print(results)
