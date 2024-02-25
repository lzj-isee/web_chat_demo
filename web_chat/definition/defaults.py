import os, json

try:
    with open("api_keys.json", mode = "r") as f:
        data  = json.load(f)
except:
    data = None


if GLM_API_KEY:= os.getenv("GLM_API_KEY") is None:
    GLM_API_KEY = data["GLM"]

if QWEN_API_KEY := os.getenv("QWEN_API_KEY") is None:
    QWEN_API_KEY = data["QWEN"]