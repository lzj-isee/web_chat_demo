import os, json
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"

from duckduckgo_search import DDGS

with DDGS() as ddgs:
    results = [r for r in ddgs.text("战地2042 M5A3的推荐配件", max_results = 8, region = "cn-zh", backend = "api")]
    # results = [r for r in ddgs.answers("战地2042 M5A3的推荐配件")]
    print(json.dumps(results, ensure_ascii = False, indent = 4))

from langchain_community.document_loaders import AsyncHtmlLoader

urls = [_result["href"] for _result in results]
loader = AsyncHtmlLoader(urls)
docs = loader.load()

debug = 1