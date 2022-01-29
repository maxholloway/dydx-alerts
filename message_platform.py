from abc import ABC, abstractmethod
import json
import requests
import smtplib
import ssl
from typing import Any, Dict

class BaseMessagePlatform(ABC):
    def __init__(self, message_platform_config: Dict):
        self.message_platform_config = message_platform_config

    @abstractmethod
    async def send_message(self, message):
        pass

    def set_api_credentials(self, api_credentials: Dict[str, Any]):
        self.api_credentials = api_credentials
        return

class SlackMessagePlatform(BaseMessagePlatform):
    async def send_message(self, message):
        # TODO: use aiohttp
        response = requests.post(
            url=self.api_credentials["webhook_url"],
            data=json.dumps({"text": message}),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
        
        return

class EmailMessagePlatform(BaseMessagePlatform):
    async def send_message(self, message):
        from_email_address, from_email_password = self.api_credentials["from_email_address"], self.api_credentials["from_email_password"]
        to_email_address = self.message_platform_config["to_email_address"]

        # smtp_server = "smtp.gmail.com"
        # port = 587  # For starttls

        # # Create a secure SSL context
        # context = ssl.create_default_context()

        # # Try to log in to server and send email
        # try:
        #     print("here 1")
        #     server = smtplib.SMTP(smtp_server,port)
        #     print("here 2")
        #     server.ehlo() # Can be omitted
        #     server.starttls(context=context) # Secure the connection
        #     server.ehlo() # Can be omitted
        #     server.login(from_email_address, from_email_password)
            
        #     message = f"Subject: dYdX Alert!\n{message}"

            
        #     server.sendmail(from_email_address, to_email_address, message)

        # except Exception as e:
        #     # Print any error messages to stdout
        #     print(e)
        # finally:
        #     server.quit() 
        # pass

        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        message = """\
        Subject: Hi there

        This message is sent from Python."""

        print(0)
        context = ssl.create_default_context()
        print(1)
        server = smtplib.SMTP(smtp_server, port)
        # with smtplib.SMTP('smtp.gmail.com:587') as server: # smtplib.SMTP('smtp.gmail.com', 587) as server:
        print(2)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(from_email_address, from_email_password)
        server.sendmail(from_email_address, to_email_address, message)
        
        server.close()

class TelegramMessagePlatform(BaseMessagePlatform):
    pass

class DiscordMessagePlatform(BaseMessagePlatform):
    pass

def get_message_platform(message_platform_config) -> BaseMessagePlatform:
    if message_platform_config["message_platform"] == "slack":
        return SlackMessagePlatform(message_platform_config["platform_specific_config"])
    elif message_platform_config["message_platform"] == "email":
        return EmailMessagePlatform(message_platform_config["platform_specific_config"])
    else:
        raise ValueError(f"Unknown message platform {message_platform_config['message_platform']}.")

if __name__ == "__main__":
    import asyncio
    with open("api_credentials.json", "r") as creds_file:
        creds = json.load(creds_file)
        WEBHOOK_URL = creds["user_id1"]["slack"]["0"]["webhook_url"]
        
    slack_msg_plat = SlackMessagePlatform({})
    slack_msg_plat.set_api_credentials({"webhook_url": WEBHOOK_URL})
    asyncio.run(slack_msg_plat.send_message("Hi there"))
    