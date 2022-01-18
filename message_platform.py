from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseMessagePlatform(ABC):
    @abstractmethod
    async def send_message(self, message):
        pass

    @abstractmethod
    async def set_api_credentials(self, api_credentials: Dict[str, Any]):
        pass

    pass

class EmailMessagePlatform(BaseMessagePlatform):
    pass

class TelegramMessagePlatform(BaseMessagePlatform):
    pass

class DiscordMessagePlatform(BaseMessagePlatform):
    pass

def get_message_platform(message_platform_config) -> BaseMessagePlatform:
    pass