import requests
import urllib3
import pickle

#information about current user
class HPC_User:
    def __init__(self):
        self.self_auth

    def error_display():
        pass

    def get_credentials():
        confirm = 0
        print("Please Enter Your Credentials: ")

        while confirm == 0:
            user_name = input("Username: ")
            password = input("Password: ")
            confirm = input("Is the above information correct? (Y/n): ")
            
            if confirm != "Y" and confirm != "n":
                confirm = input("Is the above information correct? (Y/n): ")

            if confirm == "Y":
                confirm = 1

#disable the authentication warnings
urllib3.disable_warnings()
response = requests.get("https://ansible.vai.org:8043/api/v2/hosts/89/ansible_facts/", verify=False)