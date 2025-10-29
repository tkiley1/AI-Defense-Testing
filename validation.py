import json
import os
import requests
from dotenv import load_dotenv

# Load env from .env if present
load_dotenv()


def valiation(content):
    url = "https://us.api.inspect.aidefense.security.cisco.com/api/v1/inspect/chat"

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "metadata": {},
        "config": {}
    })
    headers = {
        'X-Cisco-AI-Defense-API-Key': os.environ.get('CISCO_AI_DEFENSE_API_KEY', ''),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        data = response.json()
    except ValueError:
        return False, "Validation service returned non-JSON response."

    is_safe = bool(data.get("is_safe", True))
    if not is_safe:
        classifications = data.get("classifications")
        if classifications is None:
            return False, "Blocked by validation."
        return False, json.dumps(classifications)
    return True, "OK"
