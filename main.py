import asyncio
import json
from typing import Any, Dict, List

from dydx3 import Client
from dydx3.constants import API_HOST_ROPSTEN
from dydx3.constants import NETWORK_ID_ROPSTEN

from constants import ApiNames, PERP_MARKETS, DEFAULT_DYDX_API_KEY_CONFIG_ID
from event_trigger import get_message_generator
from message_platform import get_message_platform

async def get_stablecoin_prices():
    # TODO: get the stablecoin prices needed for dYdX
    return

async def get_index_price(perp_name: str, stable_coin_prices) -> float:
    # TODO: get the index price using the dYdX API
    await asyncio.sleep(.5)
    return 5_000

async def get_all_index_prices() -> Dict[str, float]:
    stablecoin_prices = await get_stablecoin_prices()
    index_prices = await asyncio.gather(
        *[get_index_price(perp_market, stablecoin_prices) for perp_market in PERP_MARKETS]
    )
    market_to_index_price = {PERP_MARKETS[i]: index_prices[i] for i in range(len(PERP_MARKETS))} # TODO: start async task, but don't await it
    return market_to_index_price

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
    all_api_credentials = all_api_credentials[user_id][platform_name][message_platform_api_key_config_id]
    return all_api_credentials

def get_dydx_api_credentials(user_id):
    api_credentials = get_api_credentials(user_id, ApiNames.DYDX, DEFAULT_DYDX_API_KEY_CONFIG_ID)
    return {
        "key": api_credentials["key"],
        "secret": api_credentials["secret"],
        "passphrase": api_credentials["passphrase"]
    }

def get_dydx_client(user_id):
    dydx_api_credentials = get_dydx_api_credentials(user_id)
    return Client(
        host=API_HOST_ROPSTEN,
        network_id=NETWORK_ID_ROPSTEN,
        api_key_credentials=dydx_api_credentials
    )

async def get_user_positions(user_id) -> Dict[str, float]:
    client = get_dydx_client(user_id)
    all_position_data = client.private.get_positions().data["positions"]
    positions = {pos["market"]: float(pos["size"]) for pos in all_position_data}
    return positions
    
async def get_all_users_positions(user_ids) -> Dict[str, Dict[str, float]]:
    user_ids = list(user_ids)
    user_positions = await asyncio.gather(
        *[get_user_positions(user_id) for user_id in user_ids] # list of coroutines
    )
    user_to_positions = {user_ids[i]: user_positions[i] for i in range(len(user_ids))}
    return user_to_positions

async def get_user_equity(user_id) -> float:
    client = get_dydx_client(user_id)
    return float(client.private.get_accounts().data["accounts"][0]["equity"])

async def get_all_users_equity(user_ids) -> Dict[str, float]:
    user_ids = list(user_ids)
    user_equities = await asyncio.gather(
        *[get_user_equity(user_id) for user_id in user_ids] # list of coroutines
    )
    user_to_equity = {user_ids[i]: user_equities[i] for i in range(len(user_ids))}
    return user_to_equity


async def handle_messaging(user_id, index_prices, user_equity, user_positions, message_platform_config, event_trigger_config):
    """
    * Create an event trigger object from the event trigger config.
    * Check, via builtin method of the trigger object, if the account meets criteria to send message. If it does not meet the criteria, return the empty string. If it does meet the criteria, return the message to be sent.
    * If the message is non-empty, then create a message platform object (via its config). With that object, invoke a "send_message" method.
    """
    message_generator = get_message_generator(event_trigger_config)
    message = message_generator(index_prices, user_equity, user_positions)
    if message:
        # get message platform API credentials
        message_platform_name = message_platform_config["message_platform"]
        message_platform_api_key_config_id = message_platform_config["api_key_config_id"]
        message_api_credentials = get_api_credentials(user_id, message_platform_name, message_platform_api_key_config_id)

        message_platform = get_message_platform(message_platform_config)
        message_platform.set_api_credentials(message_api_credentials)
        await message_platform.send_message(message)

async def main():
    index_prices = await get_all_index_prices()
    messenger_blobs = get_messenger_blobs()
    user_ids = get_all_user_ids(messenger_blobs)
    (all_positions, all_equity) = await asyncio.gather(
        get_all_users_positions(user_ids),
        get_all_users_equity(user_ids)
    )

    message_producers = [] # a list of coroutines
    for messenger_blob in messenger_blobs:
        user_id = messenger_blob["user_id"]
        user_positions = all_positions[user_id]
        user_equity = all_equity[user_id]
        message_platform_config = messenger_blob["message_platform_config"]
        event_trigger_config = messenger_blob["event_trigger_config"]
        message_producers.append(
            handle_messaging(user_id, index_prices, user_equity, user_positions, message_platform_config, event_trigger_config)
        )
    await asyncio.gather(*message_producers) # DONE: start async task, but don't await it

if __name__ == "__main__":
    asyncio.run(main())