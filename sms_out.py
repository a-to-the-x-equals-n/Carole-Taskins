import smtplib
from email.mime.text import MIMEText
from util import load_vars

def send_sms_via_email(to_number, carrier_gateway = "vtext.com"):
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username, smtp_password = load_vars("EMAIL", "PASSWORD")

    # Construct the email
    to_email = f"{to_number}@{carrier_gateway}"
    msg = MIMEText(message())
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = ""

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())
        server.quit()
        print("SMS sent successfully!")
    except Exception as e:
        print(f"Failed to send SMS: {e}")


def message():
    msg = f"""
    Hello!\nMy name is Carole Taskins, the Task Queen!\nI'm currently under development, but I'll be up and running soon.
    """
    return msg



if __name__ == "__main__":
    # Example usage
    send_sms_via_email("9104592653")