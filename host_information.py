#possibly need to run pip install pandas, openpyxl
import requests
import urllib3
import json
import pandas as pd
import xlsxwriter
from openpyxl import load_workbook

#create data structure to hold repeated information
class API_data:
    def __init__(self, b_token):
        self.b_token = b_token,
        self.host_lst = []
        self.headers = {
            "Authorization": f"Bearer {b_token}",
            "Content-Type": "application/json"
        }
        self.df_list = []

    #add hosts to host_lst from each page of the API
    def get_hosts(self, url):
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
                self.get_hosts(next_url)
            else:
                self.get_facts()

    #iterate through hosts to get each of the facts for that host
    def get_facts(self):
        host_label = []
        count_hosts = 0
        new_excel_file = 'host_information_test002.xlsx'
        with pd.ExcelWriter(new_excel_file, engine='xlsxwriter') as writer:

            for host_no in self.host_lst[:1]:
                hn = f'Host {host_no}'
                url = f'https://ansible.vai.org:8043/api/v2/hosts/{host_no}/ansible_facts'
                r = requests.get(url, headers=self.headers, verify=False)
                if r.status_code == 200:
                    r_json = r.json()
                    df = pd.json_normalize(r_json) 
                    
                    for i in range(len(df)):
                        host_label.append(hn)
                        host_label.T.to_excel(writer, sheet_name=hn)
        
                    df.T.to_excel(writer, startcol=1, index_label=hn, sheet_name=hn)
                    print(f"successfully saved Host {hn} data to spreadsheet")
                    count_hosts += 1

        print(f'Number of hosts saved: {count_hosts}')


#suppress warnings and set parameters
urllib3.disable_warnings()
b_token = input("Enter Bearer Token: ")
data = API_data(b_token=b_token)
data.get_hosts( url = 'https://ansible.vai.org:8043/api/v2/hosts/')