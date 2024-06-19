from util import load_vars
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import imaplib
import re
import email
import asyncio
import db as fire


class SMS:
    __EMAIL, __PASSWORD = load_vars("EMAIL", "PASSWORD")
    temp = None
    online = False

    @classmethod
    async def connect(cls):
        if not cls._Read.IMAP:
            await cls._Read.__login()
        if not cls._Write.SMTP:
            await cls._Write.__login()
        cls.online = True

    @classmethod
    async def disconnect(cls):
        if cls._Read.IMAP:
            await cls._Read.__logout()
        if cls._Write.SMTP:
            await cls._Write.__logout()
        cls.online = False


    ''' Nested IMAP Class'''

    class _Read:
        IMAP = None
        temp_user = None
        
        @classmethod
        async def __login(cls):
            cls.IMAP = imaplib.IMAP4_SSL("imap.gmail.com")
            cls.IMAP.login(SMS.__EMAIL, SMS.__PASSWORD)
            cls.IMAP.select("inbox")
        
        @classmethod
        async def __logout(cls):
            cls.IMAP.close()
            cls.IMAP.logout()
            cls.IMAP = None

        @classmethod
        async def scan(cls, users):
            # Search for Google Voice SMS emails
            parallels = [cls.__read_sms(user) for user in users]
            await asyncio.gather(*parallels)
                    
        @classmethod
        async def __read_sms(cls, user):
            sms_list = []  # List to accumulate SMS contents

            status, messages = cls.IMAP.search(None, f'FROM "{user["phone_num"]}" UNSEEN')
            if status == "OK" and messages[0].split():
                user["sms"] = messages

                for email_msg_id in user['sms'][0].split(): # Iterate over each email ID
                    _, msg_data = cls.IMAP.fetch(email_msg_id, "(RFC822)")
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # Extract the SMS content from the email
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":  # Extract plain text content
                                body = part.get_payload(decode = True).decode()
                                cls.IMAP.store(email_msg_id, '+FLAGS', '\\Seen') # Mark as read
                                sms_list.append(cls.__extract_sms_helper(body))  # Add to list
                    else:
                        body = msg.get_payload(decode = True).decode()
                        cls.IMAP.store(email_msg_id, '+FLAGS', '\\Seen')  # Mark as read
                        sms_list.append(cls.__extract_sms_helper(body))  # Add to list
            
                user['sms'] = sms_list
                await SMS._Processing.process(user)

        @classmethod
        def __extract_sms_helper(cls, email_body):
            end_phrases = [
            "YOUR ACCOUNT",
            "To respond to this text message, reply to this email or visit Google Voice."
            ]
            # Find the earliest occurrence of any end phrase
            end = len(email_body)
            for phrase in end_phrases:
                position = email_body.find(phrase)
                if position != -1 and position < end:
                    end = position
            
            return email_body[28:end].strip()

    ''' Nested SMTP Class'''

    class _Write:

        PORT = 465
        SERVER = 'smtp.gmail.com'
        SMTP = None

        @classmethod
        async def __login(cls):
            cls.SMTP = smtplib.SMTP_SSL(cls.SERVER, cls.PORT)
            cls.SMTP.login(SMS.__EMAIL, SMS.__PASSWORD)

        @classmethod
        async def __logout(cls):
            cls.SMTP.quit()
            cls.SMTP = None

        @classmethod
        async def __send(cls, user, response):
            # Format phone number in prep for Email to SMS gateways
            format_number = re.sub(r'\D', '', str(user['phone_num']))
            # Construct the email
            recv_addr = f"{format_number}{user['carrier']}"
            msg = MIMEText(response)
            msg['From'] = SMS.__EMAIL
            msg['To'] = recv_addr
            msg['Subject'] = ""

            try:
                cls.SMTP.sendmail(SMS.__EMAIL, recv_addr, msg.as_string())
                print("SMS sent successfully!")
            except Exception as e:
                print(f"Failed to send SMS: {e}")
 
    ''' Process and Route to the Appropriate Functions '''

    class _Processing:
        
        @classmethod
        async def _new(cls, user, task):
            if task:
                task_id = await fire.new_task(user['name'], task)
                response = f'Task {task_id}: "{task}" created successfully!'
                await SMS._Write.__send(user, response)
            else:
                await cls._error(user)

        @classmethod
        async def _list(cls, user, _):
            tasks = await fire.list_tasks(user['name'])
            if tasks:
                response = "Here's a list of your tasks:\n"
                for task in tasks:
                    response += f"  {task['id']}: {task['details']}\n"
            else:
                response = "You currently have no tasks."
            await SMS._Write.__send(user, response)

        @classmethod
        async def _del(cls, user, args):
            if args:
                task_id = args[0]
                await fire.del_task(user['name'], task_id)
                response = f'Task "{task_id}" deleted!'
                await SMS._Write.__send(user, response)
            else:
                await cls._error(user)

        @classmethod
        async def _help(cls, user, _):
            d = f"'del' followed by a task ID will remove it."
            n = f"'new' then a description will create a task."
            l = f"'list' will return all current tasks."
            response = f'{d}\n{n}\n{l}'
            await SMS._Write.__send(user, response)

        @classmethod
        async def _error(cls, user):
            response = f'Unrecognized message.\nPlease try again.'
            await SMS._Write.__send(user, response)
            await cls._help(user)

        COMMAND_FUNCTIONS = {
            "new": _new, 
            "list": _list, 
            "help": _help,
            "del": _del 
        }

        @classmethod
        async def process(cls, user):
            parallels = []
            for sms in user['sms']:
                parts = sms.split()
                cmd = parts[0].lower()
                args = parts[1:] if parts[1:] else None

                if cmd in cls.COMMAND_FUNCTIONS:
                    parallels.append(cls.COMMAND_FUNCTIONS[cmd](user, args))
                else:
                    parallels.append(cls._error(user))

            await asyncio.gather(*parallels)


async def main():
    await SMS.connect()
    users = [{'phone_num': '1234567890', 'carrier': '@txt.att.net', 'name': 'John Doe'}]
    await SMS._Read.scan(users)
    await SMS.disconnect()

if __name__ == "__main__":
    asyncio.run(main())