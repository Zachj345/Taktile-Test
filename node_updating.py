import os
import requests
import json

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

API_KEY = config['api_key']
URL = config['base_url']
FLOW_ID = config['flow_id']


def update_node(node_id, script_path):
    with open(script_path, 'r') as file:
        script_content = file.read()

    url = f"{URL}/flows/{FLOW_ID}/nodes/{node_id}"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Api-Key": API_KEY
    }
    payload = {
        "type": "code",
        "config": {
            "code": script_content
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    print(response.status_code)
    print(response.text)

    return response.json()


def get_python_files(directory):
    py_files = []

    for root, dirs, files, in os.walk(directory):
        for i in files:
            if i.endswith(".py"):
                py_files.append(os.path.join(root, i))
    return py_files


def main():
    test_node_id = config["node_id"]
    # Get all Python files in current dir and sub-dirs
    py_files = get_python_files('.')

    # Map of file names to node IDs
    file_to_node = {
        'script1.py': test_node_id,
        'script2.py': test_node_id,
        # Add more mappings as needed
    }

    for path in py_files:
        file_name = os.path.basename(path)
        if file_name in file_to_node:
            node_id = file_to_node[file_name]
            result = update_node(node_id, path)
            print(f"Updated node {node_id} with {file_name}: {result}")
        else:
            print(f"No node ID mapping found for {file_name}")


if __name__ == "__main__":
    main()
