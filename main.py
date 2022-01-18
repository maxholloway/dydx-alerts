import json
from typing import Any, Dict, List

from constants import ApiNames, PERP_MARKETS, DEFAULT_DYDX_API_KEY_CONFIG_ID
from event_trigger import get_message_generator
from message_platform import get_message_platform

async def get_stablecoin_prices():
    return

async def get_index_price(perp_name: str, stable_coin_prices) -> float:
    return # get the index price using the dYdX API

async def get_all_index_prices() -> Dict[str, float]:
    stablecoin_prices = await get_stablecoin_prices()    
    index_prices = {}
    for perp_market in PERP_MARKETS:
        index_prices[perp_market] = start(get_index_price(perp_market, stablecoin_prices)) # TODO: start async task, but don't await it
    return index_prices

def get_messenger_blobs() -> List[Dict[str, Any]]:
    """
    Parse messenger blobs from our local database.
    """
    # TODO: if necessary, migrate this to a db instead of a single json file
    with open("messenger_blobs.json", "r") as messenger_blobs_file:
        messenger_blobs = json.load(messenger_blobs_file)
    return messenger_blobs

def get_all_user_ids(messenger_blobs):
    user_ids = set()
    for messenger_blob in messenger_blobs:
        user_ids.add(messenger_blob["user_id"])
    return user_ids

def get_api_credentials(user_id, platform_name, message_platform_api_key_config_id):
    """
    Get the api credentials for this user on this platform with this config id.
    
    The platform could be 'dydx', in which case we will retrieve the user's API keys for accessing private dYdX APIs.
    
    The platform could be a messaging platform, in which case we will retrieve API keys/urls for accessing the messaging APIs.
    """
    # TODO: potentially replace with an encrypted database
    with open("api_credentials.json", "r") as api_credentials_file:
        all_api_credentials = json.load(api_credentials_file)
    return all_api_credentials[user_id][platform_name][message_platform_api_key_config_id]

async def get_user_positions(user_id) -> Dict[str, float]:
    dydx_api_credentials = get_api_credentials(user_id, ApiNames.DYDX, DEFAULT_DYDX_API_KEY_CONFIG_ID)
    # TODO: implement API calls to get open positions, given the user's dYdX API credentials
    return

async def get_all_users_positions(user_ids) -> Dict[str, Dict[str, float]]:
    user_to_positions = {}
    for user_id in user_ids:
        user_to_positions[user_id] = start(get_user_positions(user_id)) # TODO: start async task, but don't await it
    return user_to_positions

async def handle_messaging(user_id, index_prices, user_positions, message_platform_config, event_trigger_config):
    """
    * Create an event trigger object from the event trigger config.
    * Check, via builtin method of the trigger object, if the account meets criteria to send message. If it does not meet the criteria, return the empty string. If it does meet the criteria, return the message to be sent.
    * If the message is non-empty, then create a message platform object (via its config). With that object, invoke a "send_message" method.
    """
    message_generator = get_message_generator(event_trigger_config)
    message = message_generator(index_prices, user_positions)
    if message != "":
        # get message platform API credentials
        message_platform_name = message_platform_config["message_platform"]
        message_platform_api_key_config_id = message_platform_config["api_key_config_id"]
        message_api_credentials = get_api_credentials(user_id, message_platform_name, message_platform_api_key_config_id)

        message_platform = get_message_platform(message_platform_config)
        message_platform.set_api_credentials(message_api_credentials)
        await message_platform.send_message(message)
    return

async def main():
    index_prices = await get_all_index_prices()
    messenger_blobs = get_messenger_blobs()
    user_ids = get_all_user_ids(messenger_blobs)
    all_positions = await get_all_users_positions(user_ids)

    for messenger_blob in messenger_blobs:
        user_id = messenger_blob["user_id"]
        user_positions = all_positions[user_id]
        message_platform_config = messenger_blob["message_platform_config"]
        event_trigger_config = messenger_blob["event_trigger_config"]
        start(handle_messaging(user_id, index_prices, user_positions, message_platform_config, event_trigger_config)) # TODO: start async task, but don't await it
    return

if __name__ == "__main__":
    main() # TODO: figure out how to run the outermost asyncio event loop