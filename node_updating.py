import os
import requests
import json
from urllib.parse import urljoin


API_KEY = os.environ['API_KEY'].strip('"')
# since there's no sensitive data here I'm just going to hardcode it
URL = "https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/patch-decision-graph/sandbox/decide"
FLOW_ID = os.environ['FLOW_ID'].strip('"')
NODE_ID = os.environ['NODE_ID'].strip('"')

excluded_files = ["node_updating.py", "api_testing.py"]

default_node_id = NODE_ID


def get_node_id(file_name):
    if file_name in excluded_files:
        return None
    node_name = file_name[:-3].upper()
    env_var_name = f'NODE_ID_{node_name}'
    # using default node ID as we weren't provided others in the api docs
    try:
        return os.environ.get(env_var_name, NODE_ID)

    except:  # looking for a key error but any errors should return the default
        return NODE_ID


def update_node(node_id, script_path):
    with open(script_path, 'r') as file:
        script_content = file.read()

    url = URL
    print(f"script content {script_content}")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Api-Key": API_KEY
    }
    payload = {
        "data": {
            "node_id": node_id,
            "flow_id": FLOW_ID,
            "src_code": script_content
        },
        "metadata": {
            "version": "v1.0",
            "entity_id": "string"
        },
        "control": {
            "execution_mode": "sync"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code)
    print(response.text)

    return response.json()


def get_python_files(directory):
    py_files = []

    for root, dirs, files, in os.walk(directory):
        for i in files:
            if i.endswith(".py") and i not in excluded_files:
                py_files.append(os.path.join(root, i))
    return py_files


def main():
    test_node_id = NODE_ID
    # get all python files in current dir and sub-dirs
    py_files = get_python_files('.')
    print(f"found python files here:, {py_files}")
    # print first and last 5 characters of API key to verify we have access
    print(f"API Key: {API_KEY[:5]}...{API_KEY[-5:]}")
    print(f"Base URL: {URL}")
    print(f"Flow ID: {FLOW_ID}")
    print(f"Node ID: {NODE_ID}")

    for path in py_files:
        file_name = os.path.basename(path)
        node_id = get_node_id(file_name)
        if node_id:
            try:
                result = update_node(node_id, path)
                print(f"updated node {node_id} with {file_name}: {result}")
                excluded_files.append(file_name)
                print(excluded_files)
            except requests.exceptions.RequestException as e:
                print(f"error updating node for {file_name}: {e}")
        else:
            print(f"No node ID mapping found for {file_name}")


if __name__ == "__main__":
    main()
