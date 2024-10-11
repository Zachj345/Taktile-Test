import requests
import os
import json

with open(".github/workflows/config.json", "r") as config_file:
    config = json.load(config_file)

print(config["api_key"])
url = "https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/list-decision-graphs/sandbox/decide"
headers = {
    "accept": 'application/json',
    'Content-Type': 'application/json',
    "X-Api-Key": config["api_key"]
}

body = {
    "data": {
        "organization_name": "NB36"
    },
    "metadata": {
        "version": "v1.0",
        "entity_id": "string"
    },
    "control": {
        "execution_mode": "sync"
    }
}

url2 = "https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/get-decision-graph/sandbox/decide"

body2 = {
    "data": {
        "flow_id": config["flow_id"]
    },
    "metadata": {
        "version": "v1.0",
        "entity_id": "string"
    },
    "control": {
        "execution_mode": "sync"
    }
}

second_test_req = requests.post(url2, headers=headers, data=json.dumps(body2))
print(second_test_req.status_code)
print(second_test_req.text)
print(second_test_req)

req = requests.post(url, headers=headers, data=json.dumps(body))

# print(req.status_code)
# print(req.text)
# print(req)
