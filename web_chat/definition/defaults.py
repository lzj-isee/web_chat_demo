import os, json



if GLM_API_KEY:= os.getenv("GLM_API_KEY") is None:
    with open("api_keys.json", mode = "r") as f:
        GLM_API_KEY = json.load(f)["GLM"]