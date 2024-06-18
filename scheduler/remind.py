import requests
import os

def reminder():
    url = os.getenv("CLOUD_RUN_URL")

    try:
        response = requests.get(url) 
        
    except requests.exceptions.RequestException as e:
        print(f"Request to {url} failed: {e}")

if __name__ == "__main__":
    reminder()
