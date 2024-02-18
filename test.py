from web_chat.robots.intent import IntentRobot
from web_chat.robots.search import SearchRobot
from web_chat.robots.worker import WorkerRobot
from web_chat.robots.server import ServerRobot
from web_chat.retrieval.duckduckgo import DuckDuckGo
from web_chat.llm.glm import default_glm_3_turbo, default_glm_4_turbo
from web_chat.definition.dataframe import RetrievalResult, QueryIntent
from loguru import logger
from dataclasses import asdict

import asyncio, functools, json, os
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"

intent_robot = IntentRobot(llm = default_glm_4_turbo)
search_robot = SearchRobot(llm = default_glm_4_turbo)
worker_robot = WorkerRobot(llm = default_glm_4_turbo)
server_robot = ServerRobot(llm = default_glm_4_turbo)
search_engine = DuckDuckGo(max_results = 5, region = "cn-zh")

def web_chat(query: str) -> str:
    messages = [
        {
            "role": "user", 
            "content": query
        }
    ]
    query_intent: QueryIntent = intent_robot.infer(messages = messages)
    if query_intent != QueryIntent.WEB:
        final_response: str = default_glm_4_turbo.chat(messages = messages)
        return final_response
    else:
        pass
    logger.info("Intent stage, done")

    retrieval_queries: list[str] = search_robot.infer(messages = messages)
    logger.info(f"Search query rewrite stage, done")
    logger.info(f"retrieval_queries: {json.dumps(retrieval_queries, ensure_ascii = False, indent = 4)}")

    tasks = [
        search_engine.async_retrieve(query = retrieval_query)
        for retrieval_query in retrieval_queries
    ]
    loop = asyncio.get_event_loop()
    retrieval_results: list[list[RetrievalResult]] = loop.run_until_complete(asyncio.gather(*tasks))
    retrieval_results: list[RetrievalResult] = functools.reduce(lambda x, y: x + y, retrieval_results)
    logger.info(f"DuckDuckGo search stage, done")
    logger.info(f"retrieval_results: {json.dumps([asdict(_x) for _x in retrieval_results], ensure_ascii = False, indent = 4)}")

    # tasks = [
    #     worker_robot.async_infer(
    #         query = query, 
    #         retrieval_result = retrieval_result
    #     )
    #     for retrieval_result in retrieval_results
    # ]
    # citations: list[str | None] = loop.run_until_complete(asyncio.gather(*tasks))
    # citations: list[str] = [citation for citation in citations if citation]
    citations: list[str | None] = [
        worker_robot.infer(
            query = query, 
            retrieval_result = retrieval_result
        )
        for retrieval_result in retrieval_results
    ]
    citations: list[str] = [citation for citation in citations if citation]
    logger.info(f"Worker stage, done")
    logger.info(f"citations: {json.dumps(citations, ensure_ascii = False, indent = 4)}")

    if not citations:
        final_response: str = default_glm_4_turbo.chat(messages = messages)
        return final_response
    else:
        pass
    final_response = server_robot.infer(
        chat_history = messages, 
        citations = citations
    )
    logger.info(f"Server stage, done")
    return final_response

query = "战舰世界 大和号推荐加点和配件"
try:
    response = web_chat(query = query)
except Exception as error:
    logger.exception(error)
print(response)