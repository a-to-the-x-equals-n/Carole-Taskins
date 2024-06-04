from api.util import load_vars
import imaplib
import email
from email.mime.text import MIMEText
import smtplib
import re

class SMS_bot:

    # Temporary User object for access to name and phone number
    temp_user = None

    def __init__(self):
        self.EMAIL, self.PASSWORD = load_vars("EMAIL", "PASSWORD")
        self.IMAP = imaplib.IMAP4_SSL("imap.gmail.com") # IMAP : Internet Message Access Protocol
        self.SMTP = 'smtp.gmail.com' # SMTP : Simple Mail Transfer Protocol
        self.PORT = 587
        

    def __login(self):
        self.IMAP.login(self.EMAIL, self.PASSWORD)
        self.IMAP.select("inbox")
    

    def __logout(self):
        self.IMAP.logout()
        self.IMAP.close()


    ''' Inbound Email Functions '''


    def check_messages(self, users):
        self.__login()

        # Search for Google Voice SMS emails
        for user in users:
            status, messages = self.IMAP.search(None, f'FROM "{user.phone_num}" UNSEEN')
            if status == "OK":
                SMS_bot.temp_user = user
                self.__extract_sms(messages)

        self.__logout()


    def __extract_sms(self, messages):

        for email_msg_id in messages[0].split():
            _, msg_data = self.IMAP.fetch(email_msg_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Extract the SMS content from the email
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode = True).decode()
                        sms = self.__extract_sms_helper(body)
            else:
                body = msg.get_payload(decode = True).decode()
                sms = self.__extract_sms_helper(body)

            # Mark the email as read
            self.IMAP.store(email_msg_id, '+FLAGS', '\\Seen')
            self.__build_reply(sms)


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


    ''' Outbound Email Functions '''


    def __build_reply(self, sms):

        # TODO : write functionality to handle different commands from user

        # Format phone number in prep for Email to SMS gateways
        format_number = re.sub(r'\D', '', SMS_bot.temp_user.phone_num)

        # Construct the email
        recv_addr = f"{format_number}{SMS_bot.temp_user.carrier}"
        msg = MIMEText(self.__default_message())
        msg['From'] = self.EMAIL
        msg['To'] = recv_addr
        msg['Subject'] = ""

        try:
            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(self.SMTP, self.PORT)
            server.starttls()
            server.login(self.EMAIL, self.PASSWORD)
            server.sendmail(self.EMAIL, recv_addr, msg.as_string())
            server.quit()
            print("SMS sent successfully!")

        except Exception as e:
            print(f"Failed to send SMS: {e}")


    @staticmethod
    def __default_message():
        msg = f"""
        Hello {SMS_bot.temp_user.f_name}!\nMy name is Carole Taskins\nI'm currently under development, but hopefully I'll be up and running very soon.
        """
        return msg


