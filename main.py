from sms_in import check_email_for_sms
from sms_out import send_sms_via_email
from time import sleep

def main():

    sender = check_email_for_sms()

    if sender != None:
        send_sms_via_email(sender)

        
        
if __name__ == "__main__":
    main()