import requests

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
            self.COMMAND_FUNCTIONS[cmd](endpoint = cmd, params = args, headers = user.name.lower())
        else:
            self.post(endpoint = "error")
        
    
    def post(self, endpoint, params = None, headers = None):
        url = f"{self.base_url}/{endpoint}"
        requests.post(url, headers = headers, params = params)
        

    def get(self, endpoint, params = None, headers = None):
        url = f"{self.base_url}/{endpoint}"
        return requests.get(url, headers = headers, params = params)


    def delete(self, endpoint, params = None, headers = None):
        url = f"{self.base_url}/{endpoint}"
        requests.delete(url, headers = headers, params = params)

    def get_users(self, endpoint = "users", params = None, headers = None):
        url = f"{self.base_url}/{endpoint}"
        return requests.get(url, headers = headers, params = params)

