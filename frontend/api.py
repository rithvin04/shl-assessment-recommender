import requests

BACKEND_URL = "http://127.0.0.1:8000/chat"


def send_message(messages):

    response = requests.post(
        BACKEND_URL,
        json={"messages": messages}
    )

    response.raise_for_status()

    return response.json()