from abc import ABC, abstractmethod
import json
import requests
from typing import Any, Dict

class BaseMessagePlatform(ABC):
    @abstractmethod
    async def send_message(self, message):
        pass

    def set_api_credentials(self, api_credentials: Dict[str, Any]):
        self.api_credentials = api_credentials
        return

class SlackMessagePlatform(BaseMessagePlatform):
    def __init__(self, slack_config):
        self.config = slack_config

    async def send_message(self, message):
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
    pass

class TelegramMessagePlatform(BaseMessagePlatform):
    pass

class DiscordMessagePlatform(BaseMessagePlatform):
    pass

def get_message_platform(message_platform_config) -> BaseMessagePlatform:
    if message_platform_config["message_platform"] == "slack":
        return SlackMessagePlatform(message_platform_config["platform_specific_config"])

if __name__ == "__main__":
    import asyncio
    with open("api_credentials.json", "r") as creds_file:
        creds = json.load(creds_file)
        WEBHOOK_URL = creds["user_id1"]["slack"]["0"]["webhook_url"]
        
    slack_msg_plat = SlackMessagePlatform({})
    slack_msg_plat.set_api_credentials({"webhook_url": WEBHOOK_URL})
    asyncio.run(slack_msg_plat.send_message("Hi there"))
    