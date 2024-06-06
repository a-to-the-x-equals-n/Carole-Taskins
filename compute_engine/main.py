from compute_engine.models.imap import IMAPbot
from models.client import HttpClient
from time import sleep


def main():

    client = HttpClient("1")
    users = client.get_users()

    try:
        IMAPbot.login()

        while True:
            
            for user in IMAPbot.check_messages(users):
                client.process_request(user)

            sleep(.5)

    finally:
        IMAPbot.logout()


