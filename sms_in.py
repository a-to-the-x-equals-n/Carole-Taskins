import imaplib
import email
from email.header import decode_header
import re

def check_email_for_sms():
    # Connect to the email server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("task.watch.24@gmail.com", "fygr xrhk fcsp ngsc")
    mail.select("inbox")

    # Search for Google Voice SMS emails
    status, messages = mail.search(None, '(FROM "(910) 507-5707" UNSEEN)')
    # status, messages = mail.search(None, '(FROM "(910) 459-2653")')
    email_ids = messages[0].split()
    phone_number = None

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])


        # Decode the email subject to extract the phone number
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')
        phone_number = extract_phone_number(subject)
        
        # Extract the SMS content from the email
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    sms_content = extract_sms_content(body)
            
        else:
            body = msg.get_payload(decode=True).decode()
            sms_content = extract_sms_content(body)
            

        print(f"From: {phone_number}: {sms_content[28:]}")

        # Mark the email as read
        mail.store(email_id, '+FLAGS', '\\Seen')


    mail.logout()

    return phone_number



def extract_phone_number(subject):
    # Extract phone number from subject using regex for format (xxx) xxx-xxxx
    phone_number_match = re.search(r'\(\d{3}\) \d{3}-\d{4}', subject)
    if phone_number_match:
        phone_number = phone_number_match.group()
        # Remove formatting to convert to xxxxxxxxxx
        formatted_phone_number = re.sub(r'\D', '', phone_number)
        return formatted_phone_number
    return None


def extract_sms_content(email_body):
    # Find the SMS content within the email body
    # The actual SMS message usually ends before the first "To respond" line
    end_marker = "YOUR ACCOUNT"
    end_index = email_body.find(end_marker)
    if end_index != -1:
        return email_body[:end_index].strip()
    return email_body.strip()

# Example usage
check_email_for_sms()
