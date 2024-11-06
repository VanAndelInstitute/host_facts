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
        self.host_names = {}
        self.headers = {
            "Authorization": f"Bearer {b_token}",
            "Content-Type": "application/json"
        }
        self.df_list = [] #FIXME might not need

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


    def get_facts(self):

        #initialize variables
        count_hosts = 0
        col_num = 0

        for host_no in self.host_lst:
            url = f'https://ansible.vai.org:8043/api/v2/hosts/{host_no}/ansible_facts'
            r = requests.get(url, headers=self.headers, verify=False)

            if r.status_code == 200:
                r_json = r.json()
                self.host_names[host_no] = r_json['ansible_nodename']
                df = pd.json_normalize(r_json, sep=' ')

                server = f'{self.host_names[host_no]}'
                host_ids = [server] * len(df.columns)  #to add a host number alongside the information (querying)
                df.loc[-1] = host_ids
                df.index += 1
                df.sort_index()
                df = df.T

                csv_file = 'host_information.csv'
                df.to_csv(csv_file, mode='a')
                print(f"Successfully saved {server} data to host_information.csv")
                count_hosts += 1
        print(f'Number of hosts saved: {count_hosts}')


#suppress warnings and set parameters
urllib3.disable_warnings()
print("\nDelete the file 'host_information.csv' if it already exists (will be in the same file as this script)\n")
b_token = input("Enter Bearer Token: ")
data = API_data(b_token=b_token)
data.get_hosts( url = 'https://ansible.vai.org:8043/api/v2/hosts/')
