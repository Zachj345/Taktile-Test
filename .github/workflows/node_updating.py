import os
import requests
import json

with open(".github/workflows/config.json", "r") as config_file:
    config = json.load(config_file)

# this will send the new code in github to taktile


def code_to_taktile(file_path, node_id):
    url = config["url"]
    flow_id = config["flow_id"]  # copied from docs
    node_id = config["node_id"]  # copied from docs
    api_key = config["api_key"]

    print(flow_id, api_key)

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }

    if not os.path.exists(file_path):
        print(f"file at {file_path} does not exist currently")
        return

    with open(file_path, "r") as file:
        src_code = file.read()
    # src_code = "def new_function_added(): return 'new code uploaded'"

    payload = {
        "metadata": {
            "version": "v1.0",
            "entity_id": "string"
        },
        "control": {
            "execution_mode": "sync"
        },

        "data": {
            "flow_id": flow_id,
            "node_id": node_id,
            "src_code": src_code
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Code node updated successfully!", node_id)
    else:
        print(response)
        print(
            f"Failed upload with status code of {response.status_code} \n text here: {response.text}")


if __name__ == "__main__":
    # getting the updated code in github actions, and reading it here to push to taktile
    # if we were just using the 2 example files the code would look something like this below
    # with open("Multiply.py", "r") as file:
    #     updated = file.read()
    # with open("Summarize.py", "r") as second_file:
    #     second_updated = second_file.read()
    # code_to_taktile(updated)
    # code_to_taktile(second_updated)

    # using the same node ID because these were exmples in the docs and there weren't any others
    multiply_node_id = os.getenv("node_id")
    summarize_node_id = os.getenv("node_id")

    code_to_taktile("Multiply.py", multiply_node_id)
    code_to_taktile("Summarize.py", summarize_node_id)
