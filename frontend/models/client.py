import requests
import json

class HttpClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.COMMAND_FUNCTIONS = {
            "new": self.post, 
            "list": self.get, 
            "help": self.get,
            "del": self.delete 
        }


    def process_request(self, user):
        parts = user.sms.split()
        cmd = parts[0].lower()
        args = parts[1:] if parts[1:] else None

        if cmd in self.COMMAND_FUNCTIONS:
            if cmd == "new" and args:
                self.COMMAND_FUNCTIONS[cmd](endpoint = cmd, headers = {'name': user.name.lower()}, json = {'details': ' '.join(args)})
            elif cmd == "del" and args:
                task_id = args[0]
                self.COMMAND_FUNCTIONS[cmd](endpoint = f"del/{task_id}", headers = {'name': user.name.lower()})
            else:
                self.COMMAND_FUNCTIONS[cmd](endpoint = cmd, headers={'name': user.name.lower()})
        else:
            self.post(endpoint = "error")
        
    
    def post(self, endpoint, params = None, headers = None, json = None):
        url = f"{self.base_url}/{endpoint}"
        return requests.post(url, params = params, headers = headers, json = json)
        

    def get(self, endpoint, params = None, headers = None, json = None):
        url = f"{self.base_url}/{endpoint}"
        return requests.get(url, params = params, headers = headers, json = json)


    def delete(self, endpoint, params = None, headers = None, json = None):
        url = f"{self.base_url}/{endpoint}"
        requests.delete(url, params = params, headers = headers, json = json)

    def get_users(self, endpoint = "users", params = None, headers = None, json = None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params = params, headers = headers, json = json)
        return response.json()

