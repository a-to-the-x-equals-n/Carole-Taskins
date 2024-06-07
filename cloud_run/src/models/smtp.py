from compute_engine.util import load_vars
from email.mime.text import MIMEText
import smtplib
import re



class SMTPbot:

    # Temporary User object for access to name and phone number
    temp_user = None

    def __init__(self):
        self.EMAIL, self.PASSWORD = load_vars("EMAIL", "PASSWORD")
        self.SMTP = 'smtp.gmail.com' # SMTP : Simple Mail Transfer Protocol
        self.PORT = 587


    ''' Outbound Email Functions '''

    def send_sms(self, user, response):

        # TODO : write functionality to handle different commands from user

        # Format phone number in prep for Email to SMS gateways
        format_number = re.sub(r'\D', '', SMTPbot.temp_user.phone_num)

        # Construct the email
        recv_addr = f"{format_number}{SMTPbot.temp_user.carrier}"
        msg = MIMEText(self.build_reply(user, response))
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


    def build_reply(self, response):
        return self.__default_message
    

    @staticmethod
    def __default_message():
        msg = f"""
        Hello {SMTPbot.temp_user.f_name}!\nMy name is Carole Taskins\nI'm currently under development, but hopefully I'll be up and running very soon.
        """
        return msg


