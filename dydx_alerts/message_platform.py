from abc import ABC, abstractmethod
import aiohttp
import json
import os
import requests
import smtplib
import ssl
from typing import Any, Dict

from log import get_logger

class BaseMessagePlatform(ABC):
    """
    Abstract class that all messaging platforms must implement.
    """

    def __init__(self, message_platform_config: Dict, message_api_credentials: Dict):
        self.message_platform_config = message_platform_config
        self.message_api_credentials = message_api_credentials

    @abstractmethod
    async def send_message(self, message: str, logger):
        """
        Send the given free-text message. If it sends successfully, return True; else, return False.
        """
        pass


class SlackMessagePlatform(BaseMessagePlatform):
    async def send_message(self, message: str, logger):
        request_url = self.message_api_credentials["webhook_url"]
        data = json.dumps({"text": message})
        headers = {'Content-Type': 'application/json'}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(request_url, data=data, headers=headers) as resp:
                    if resp.status != 200:
                        logger.error("Slack API error occurred.")
                        logger.error(await resp.text())
                        return False
            logger.info("Successfully sent slack message.")
            return True
        except Exception as ex:
            logger.error(f"The following exception occured:\n{ex}", exc_info=True)
            return False
        

class EmailMessagePlatform(BaseMessagePlatform):
    async def send_message(self, email_body, logger):
        # TODO: support general smtp servers, not just gmail.
        try:
            from_email_address, from_email_password = self.message_api_credentials["from_email_address"], self.message_api_credentials["from_email_password"]
            to_email_address = self.message_platform_config["to_email_address"]

            port = 587
            smtp_server = "smtp.gmail.com"
            email_content = f"Subject: dYdX Alert\n\n{email_body}"

            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context)
                server.login(from_email_address, from_email_password)
                server.sendmail(from_email_address, to_email_address, email_content)
            
            logger.info("Successfully sent email message.")
            return True
        except Exception as ex:
            logger.error(f"The following exception occured:\n{ex}", exc_info=True)
            return False


class TelegramMessagePlatform(BaseMessagePlatform):
    async def send_message(self, message: str, logger):
        try:
            bot_token, tg_chat_id = self.message_api_credentials["bot_token"], self.message_api_credentials["telegram_chat_id"]
            request_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={tg_chat_id}&text={message}"

            async with aiohttp.ClientSession() as session:
                async with session.get(request_url) as resp:
                    if resp.status != 200:
                        logger.error("Telegram API error occurred.")
                        logger.error(await resp.text())
                        return False
            logger.info("Successfully sent telegram message.")
            return True
        except Exception as ex:
            logger.error(f"The following exception occured:\n{ex}", exc_info=True)
            return False


class DiscordMessagePlatform(BaseMessagePlatform):
    async def send_message(self, message: str, logger):
        try:
            request_url = os.path.join(self.message_api_credentials["webhook_url"], "slack")
            data = json.dumps({"text": message})
            headers = {'Content-Type': 'application/json'}

            async with aiohttp.ClientSession() as session:
                async with session.post(request_url, data=data, headers=headers) as resp:
                    if resp.status != 200:
                        logger.error("Discord API error occurred.")
                        logger.error(await resp.text())
                        return False
            logger.info("Successfully sent discord message.")
            return True
        except Exception as ex:
            logger.error(f"The following exception occured:\n{ex}", exc_info=True)
            return False

def get_message_platform(message_platform_config, message_api_credentials) -> BaseMessagePlatform:
    # TODO: potentially move this into a dict, instead of a case-by-case if statement.
    platform_id = message_platform_config["message_platform"].upper()
    platform_config = message_platform_config["platform_specific_config"]
    if platform_id == "SLACK":
        return SlackMessagePlatform(platform_config, message_api_credentials)
    elif platform_id == "EMAIL":
        return EmailMessagePlatform(platform_config, message_api_credentials)
    elif platform_id == "TELEGRAM":
        return TelegramMessagePlatform(platform_config, message_api_credentials)
    elif platform_id == "DISCORD":
        return DiscordMessagePlatform(platform_config, message_api_credentials)
    else:
        raise ValueError(f"Unknown message platform {message_platform_config['message_platform']}.")

if __name__ == "__main__":
    import asyncio
    from log import get_logger

    logger = get_logger()

    with open("api_credentials.json", "r") as creds_file:
        creds = json.load(creds_file)["user_id1"]["slack"][0]
        
    message_platform = SlackMessagePlatform({}, creds)
    asyncio.run(message_platform.send_message("Testing out the waters!", logger))
