from time import sleep
from models.users import User
from models.sms import SMS_bot

def main():

    while True:

        users = User.load_users()
        bot = SMS_bot
        bot.check_messages(users)

        sleep(4)
        print('sleeping...')

        
if __name__ == "__main__":
    main()