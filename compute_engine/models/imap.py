from compute_engine.util import load_vars
import imaplib
import email


class IMAPbot:

    EMAIL, PASSWORD = load_vars("EMAIL", "PASSWORD")
    IMAP = imaplib.IMAP4_SSL("imap.gmail.com")


    @classmethod
    def login(cls):
        cls.IMAP.login(cls.EMAIL, cls.PASSWORD)
        cls.IMAP.select("inbox")
    

    @classmethod
    def logout(cls):
        cls.IMAP.logout()
        cls.IMAP.close()


    @classmethod
    def check_messages(cls, users):

        # Search for Google Voice SMS emails
        for user in users:
            status, messages = cls.IMAP.search(None, f'FROM "{user.phone_num}" UNSEEN')
            if status == "OK":
                cls.temp_user = user
                user.sms = cls.__extract_sms(messages)
                yield user


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
                        return cls.__extract_sms_helper(body)
            else:
                body = msg.get_payload(decode = True).decode()
                cls.IMAP.store(email_msg_id, '+FLAGS', '\\Seen')
                return cls.__extract_sms_helper(body)


        @classmethod
        def __extract_sms_helper(email_body):
            '''
                Since I'm having Google Voice forward all SMS messages to my email, I have to ignore all of the added Google
                content included in the email.

                This function extracts the pure text messsage from the user.
            '''
            end = email_body.find("YOUR ACCOUNT")

            if end != -1:
                return email_body[28:end].strip()
            
            return email_body[28:].strip()
