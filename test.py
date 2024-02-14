from web_chat.llm.glm import default_glm_3_turbo
from web_chat.robots.search import SearchRobot
rewrite_robot = SearchRobot(llm = default_glm_3_turbo)
messages = [
    {
        "role": "user", 
        "content": "langchain 联网搜索器"
    }
]
response = rewrite_robot.infer(messages = messages)
print(response)