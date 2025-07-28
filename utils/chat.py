import requests
from config import DIFY_API_KEY, DIFY_API_URL

def ask_dify(message):
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {},
        "query": message,
        "user": "campusmate-user"
    }

    response = requests.post(DIFY_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get("answer", "No answer returned.")
    else:
        return f"Error {response.status_code}: {response.text}"
