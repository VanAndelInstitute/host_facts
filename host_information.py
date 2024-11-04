#possibly need to run pip install pandas
import requests
import urllib3
import json
import pandas as pd

#create data structure to hold repeated information
class API_data:
    def __init__(self, b_token):
        self.b_token = b_token,
        self.host_lst = []
        self.headers = {
            "Authorization": f"Bearer {b_token}",
            "Content-Type": "application/json"
        }

    #add hosts to host_lst from each page of the API
    def add_to_hosts(self, url):

        r = requests.get(url, headers=self.headers, verify=False)
        if r.status_code == 200:
            r_json = r.json()
            df = pd.json_normalize(r_json['results'])
            hosts = df['id']

            for host_no in hosts:
                self.host_lst.append(host_no)

            #if there is a next page, recurse with the url held in the 'next' field
            if r_json['next']:
                next_url = 'https://ansible.vai.org:8043' + r_json['next']
                self.add_to_hosts(next_url)


#suppress warnings and set parameters
urllib3.disable_warnings()

#parameters
host_lst = []
b_token = input("Enter Bearer Token: ")
data = API_data(b_token=b_token)

#get all the hosts
data.add_to_hosts( url = 'https://ansible.vai.org:8043/api/v2/hosts/')
print(len(data.host_lst))