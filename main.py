from time import sleep
from users import User
from emailer import Emailer

def main():

    while True:

        users = User.load_users()
        emailer = Emailer()
        emailer.check_email(users)

        sleep(4)
        print('sleeping...')

        
if __name__ == "__main__":
    main()