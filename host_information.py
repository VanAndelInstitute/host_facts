import requests
import urllib3
import json

#suppress warnings
urllib3.disable_warnings()

#tokens
b_token = input("Enter Bearer Token: ")

#arguments for request
url = "https://ansible.vai.org:8043/api/v2/hosts/1/ansible_facts/"
verify = False
headers = {
    "Authorization": f"Bearer {b_token}",
    "Content-Type": "application/json"
}

#send get request
response = requests.get(url, headers=headers, verify=verify)

if response.status_code == 200:
    response_json = response.json()
    print(json.dumps(response_json, indent=4))