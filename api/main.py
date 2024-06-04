from time import sleep
from models.users import User
from models.emailer import Emailer

def main():

    while True:

        users = User.load_users()
        emailer = Emailer()
        emailer.check_email(users)

        sleep(4)
        print('sleeping...')

        
if __name__ == "__main__":
    main()