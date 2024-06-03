from util import load_vars
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
import smtplib
import re

class Emailer:

    temp_user = None

    def __init__(self):
        self.EMAIL, self.PASSWORD = load_vars("EMAIL", "PASSWORD")
        self.MAIL = imaplib.IMAP4_SSL("imap.gmail.com")
        self.SMTP_SERVER = 'smtp.gmail.com'
        self.PORT = 587
        

    def __login(self):
        self.MAIL.login(self.EMAIL, self.PASSWORD)
        self.MAIL.select("inbox")
    

    def __logout(self):
        self.MAIL.logout()


    def check_email(self, users):
        self.__login()

        # Search for Google Voice SMS emails
        for user in users:
            status, messages = self.MAIL.search(None, f'FROM "{user.phone_num}" UNSEEN')
            if status == "OK":
                Emailer.temp_user = user
                self.__extract_sms(messages)

        self.__logout()


    def __extract_sms(self, messages):

        email_ids = messages[0].split()

        for email_id in email_ids:
            status, msg_data = self.MAIL.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            # Decode the email subject to extract the phone number
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            
            # Extract the SMS content from the email
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        sms = self.__extract_sms_helper(body)[28:]
        
            else:
                body = msg.get_payload(decode=True).decode()
                sms = self.__extract_sms_helper(body)[28:]
                
            # print(f"From: {phone_number}: {sms_content[28:]}")

            # Mark the email as read
            self.MAIL.store(email_id, '+FLAGS', '\\Seen')

            self.__build_reply()


    def __extract_sms_helper(self, email_body):
        # Find the SMS content within the email body
        end_index = email_body.find("YOUR ACCOUNT")
        if end_index != -1:
            return email_body[:end_index].strip()
        return email_body.strip()


    def __build_reply(self):
        format_number = re.sub(r'\D', '', Emailer.temp_user.phone_num)

        # Construct the email
        recv_addr = f"{format_number}{Emailer.temp_user.carrier}"
        msg = MIMEText(self.__default_message())
        msg['From'] = self.EMAIL
        msg['To'] = recv_addr
        msg['Subject'] = ""

        try:
            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(self.SMTP_SERVER, self.PORT)
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
        Hello {Emailer.temp_user.f_name}!\nMy name is Carole Taskins\nI'm currently under development, but hopefully I'll be up and running very soon.
        """
        return msg


