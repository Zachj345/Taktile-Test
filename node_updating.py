import os
import requests
import json

# Load configuration
# with open('config.json', 'r') as config_file:
#     config = json.load(config_file)

API_KEY = os.environ['API_KEY']
URL = os.environ['URL']  # Assuming this is your BASE_URL
FLOW_ID = os.environ['FLOW_ID']
NODE_ID = os.environ['NODE_ID']

excluded_files = ["node_updating.py", "api_testing.py"]

def get_node_id(file_name):
    if file_name in excluded_files:
        return None
    else:
        return NODE_ID

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
            if i.endswith(".py") and i not in excluded_files:
                py_files.append(os.path.join(root, i))
    return py_files


def main():
    test_node_id = NODE_ID
    # Get all Python files in current dir and sub-dirs
    py_files = get_python_files('.')

    for path in py_files:
        file_name = os.path.basename(path)
        node_id = get_node_id(file_name)
        if node_id:
            result = update_node(node_id, path)
            print(f"Updated node {node_id} with {file_name}: {result}")
        else:
            print(f"No node ID mapping found for {file_name}")


if __name__ == "__main__":
    main()
