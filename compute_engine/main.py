from compute_engine.models.imap import IMAPbot
from models.client import HttpClient
from models.users import User
import time


def main():

    client = HttpClient("")
    user_data = client.get_users()
    users = create_users(user_data)

    try:
        IMAPbot.login()

        while True:
            for user in IMAPbot.check_messages(users):
                client.process_request(user)

            time.sleep(0.5)

    finally:
        IMAPbot.logout()


def create_users(data):
    # Create a list to store User objects
    users = []
    
    # Iterate through the dictionary and create User objects
    for _, user_data in data.items():
        new_user = User.from_dict(user_data)
        users.append(new_user)
    
    return users