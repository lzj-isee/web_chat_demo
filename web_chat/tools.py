from datetime import datetime
import time, jwt


def generate_token(apikey: str, exp_seconds: int = 600):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm = "HS256",
        headers = {"alg": "HS256", "sign_type": "SIGN"},
    )

def get_current_datetime() -> str:
    return datetime.now().strftime('%Y-%m-%d')

if __name__ == "__main__":
    print(get_current_datetime())