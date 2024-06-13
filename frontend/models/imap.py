from util import load_vars
import imaplib
import email
from email.header import decode_header


class IMAPbot:

    EMAIL, PASSWORD = load_vars("EMAIL", "PASSWORD")
    IMAP = None
    # IMAP = imaplib.IMAP4_SSL("imap.gmail.com")
    temp_user = None


    @classmethod
    def login(cls):
        cls.IMAP = imaplib.IMAP4_SSL("imap.gmail.com")
        cls.IMAP.login(cls.EMAIL, cls.PASSWORD)
        cls.IMAP.select("inbox")
    

    @classmethod
    def logout(cls):
        if cls.IMAP is not None:
            cls.IMAP.close()
            cls.IMAP.logout()
            cls.IMAP = None
        


    @classmethod
    def check_messages(cls, users):
        
        cls.login()
     

        try:
            # Search for Google Voice SMS emails
            for user in users:
                status, messages = cls.IMAP.search(None, f'FROM "{user.phone_num}" UNSEEN')
                
                if status == "OK" and messages[0].split():
                    cls.temp_user = user
                    print(f'\n\n{user.sms}\n\n')
                    user.sms = cls.__extract_sms(messages)
                    yield user

        finally:
            cls.logout()


    @classmethod
    def __extract_sms(cls, messages):

        for email_msg_id in messages[0].split():
            _, msg_data = cls.IMAP.fetch(email_msg_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Extract the SMS content from the email
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode = True).decode()
                        cls.IMAP.store(email_msg_id, '+FLAGS', '\\Seen')
                        
                        testing = cls.__extract_sms_helper(body)
                        print(testing)
                        return testing
            else:
                body = msg.get_payload(decode = True).decode()
                cls.IMAP.store(email_msg_id, '+FLAGS', '\\Seen')
                testing = cls.__extract_sms_helper(body)
                print(testing)
                return testing


    @classmethod
    def __extract_sms_helper(cls, email_body):
        '''
            Since I'm having Google Voice forward all SMS messages to my email, I have to ignore all of the added Google
            content included in the email.

            This function extracts the pure text messsage from the user.
        '''
        end = email_body.find("YOUR ACCOUNT")

        if end != -1:
            return email_body[28:end].strip()
        
        return email_body[28:].strip()
