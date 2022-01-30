from abc import ABC, abstractmethod
import aiohttp
import json
import requests
import smtplib
import ssl
from typing import Any, Dict

class BaseMessagePlatform(ABC):
    def __init__(self, message_platform_config: Dict):
        self.message_platform_config = message_platform_config

    @abstractmethod
    async def send_message(self, message: str):
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
    async def send_message(self, email_body):
        # TODO: add error handling?
        from_email_address, from_email_password = self.api_credentials["from_email_address"], self.api_credentials["from_email_password"]
        to_email_address = self.message_platform_config["to_email_address"]

        port = 587
        smtp_server = "smtp.gmail.com"
        email_content = f"Subject: dYdX Alert\n\n{email_body}"

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(from_email_address, from_email_password)
            server.sendmail(from_email_address, to_email_address, email_content)
        print(f"Mail sent with no errors. Email content:\n{email_content}")

class TelegramMessagePlatform(BaseMessagePlatform):
    async def send_message(self, message: str):
        bot_token, tg_chat_id = self.api_credentials["bot_token"], self.api_credentials["telegram_chat_id"]
        request_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={tg_chat_id}&text={message}"

        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as resp:
                if resp.status != 200:
                    print("Telegram API error occurred.")
                    print(await resp.text())
                    return -1
                
                resp_dict = json.loads(await resp.text())

class DiscordMessagePlatform(BaseMessagePlatform):
    pass

def get_message_platform(message_platform_config) -> BaseMessagePlatform:
    if message_platform_config["message_platform"] == "slack":
        return SlackMessagePlatform(message_platform_config["platform_specific_config"])
    elif message_platform_config["message_platform"] == "email":
        return EmailMessagePlatform(message_platform_config["platform_specific_config"])
    elif message_platform_config["message_platform"] == "telegram":
        return TelegramMessagePlatform(message_platform_config["platform_specific_config"])
    else:
        raise ValueError(f"Unknown message platform {message_platform_config['message_platform']}.")

if __name__ == "__main__":
    import asyncio
    with open("api_credentials.json", "r") as creds_file:
        creds = json.load(creds_file)["user_id1"]["telegram"]["0"]
        
    message_platform = TelegramMessagePlatform({"telegram_chat_id": "-789851131"})
    message_platform.set_api_credentials(creds)
    asyncio.run(message_platform.send_message("Hi there"))
