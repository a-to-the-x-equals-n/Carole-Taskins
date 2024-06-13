from models.imap import IMAPbot
from models.client import HttpClient
from models.users import User
import time


def main():

    client = HttpClient("http://127.0.0.1:8080")
    user_data = client.get_users()

    users = create_users(user_data)

    while True:
        for user in IMAPbot.check_messages(users):
            client.process_request(user)

        time.sleep(0.1)



def create_users(data):
    # Create a list to store User objects
    users = []
    
    # Iterate through the dictionary and create User objects
    for user in data:
        new_user = User.from_dict(user)
        users.append(new_user)
    
    return users


if __name__ == '__main__':
    main()