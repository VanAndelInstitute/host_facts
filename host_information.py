#possibly need to run pip install pandas, openpyxl
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
            df = pd.json_normalize(r_json['results']) #flatten the data to pull the host ids
            hosts = df['id']
            for host_no in hosts:
                self.host_lst.append(host_no)
            
            #if there is a next page, recurse with the url held in the 'next' field
            if r_json['next']:
                next_url = 'https://ansible.vai.org:8043' + r_json['next']
                self.add_to_hosts(next_url)
            else:
                self.get_facts()

    #iterate through hosts to get each of the facts for that host
    def get_facts(self):
        for host_no in self.host_lst:
            url = f'https://ansible.vai.org:8043/api/v2/hosts/{host_no}/ansible_facts'
            r = requests.get(url, headers=self.headers, verify=False)
            if r.status_code == 200:
                r_json = r.json()
                df = pd.json_normalize(r_json) 
                self.json_to_excel(df=df)

    #create an excel file
    def json_to_excel(self, df):
        excel_file = 'host_information.xlsx'
        df.to_excel(excel_file, index=False, sheet_name='Hosts + Information')
        print(f"successfully saved data to {excel_file}")


#suppress warnings and set parameters
urllib3.disable_warnings()

#parameters
b_token = input("Enter Bearer Token: ")
data = API_data(b_token=b_token)

#get all the hosts
data.add_to_hosts( url = 'https://ansible.vai.org:8043/api/v2/hosts/')