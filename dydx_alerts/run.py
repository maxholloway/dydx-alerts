"""
Entrypoint for running the bot a single time.
"""

import asyncio
import json
from typing import Any, Dict, List, Tuple

from dydx3 import Client
from dydx3.constants import API_HOST_ROPSTEN, API_HOST_MAINNET
from dydx3.constants import NETWORK_ID_ROPSTEN, NETWORK_ID_MAINNET

from constants import ApiNames, DEFAULT_DYDX_API_KEY_CONFIG_ID
from event_trigger import get_message_generator
from oracle_price import OraclePriceGetter
from log import get_logger
from message_platform import get_message_platform


def get_messenger_blobs() -> List[Dict[str, Any]]:
    """
    Parse messenger blobs from our local database.
    """
    # TODO: if necessary, migrate this to a db instead of a single json file
    with open("messenger_blobs.json", "r") as messenger_blobs_file:
        messenger_blobs = json.load(messenger_blobs_file)
    return messenger_blobs


def get_all_user_accounts(messenger_blobs):
    """
    Parse each user account from the messenger_blobs.
    A user account is defined as the duple (user_id, network).
    For instance, the same user may have a mainnet account and
    a testnet account, and those would be treated separately.
    """
    user_accounts = set()
    for messenger_blob in messenger_blobs:
        user_accounts.add(
            (messenger_blob["user_id"], messenger_blob["dydx_config"]["environment"])
        )
    return user_accounts


def get_api_credentials(user_id, platform_name, message_platform_api_key_config_id):
    """
    Get the api credentials for this user on this platform with this config id.

    The platform could be 'dydx', in which case we will retrieve the user's API keys for accessing private dYdX APIs.

    The platform could be a messaging platform, in which case we will retrieve API keys/urls for accessing the messaging APIs.
    """
    # TODO: potentially replace with an encrypted database
    with open("api_credentials.json", "r") as api_credentials_file:
        all_api_credentials = json.load(api_credentials_file)

    # TODO: add error handling for missing credentials
    all_api_credentials = all_api_credentials[user_id][platform_name][
        message_platform_api_key_config_id
    ]
    return all_api_credentials


def get_dydx_api_credentials(user_id):
    """
    Get dYdX API credentials from api_credentials.json
    """
    api_credentials = get_api_credentials(
        user_id, ApiNames.DYDX, DEFAULT_DYDX_API_KEY_CONFIG_ID
    )
    return {
        "key": api_credentials["key"],
        "secret": api_credentials["secret"],
        "passphrase": api_credentials["passphrase"],
    }


def get_dydx_client(user_id: str, net: str):
    """
    Getter for a particular user's dYdX API client.
    """
    if net == "mainnet":
        host = API_HOST_MAINNET
        network_id = NETWORK_ID_MAINNET
    elif net == "testnet":
        host = API_HOST_ROPSTEN
        network_id = NETWORK_ID_ROPSTEN
    else:
        raise Exception("Invalid messenger_blobs.dydx_config.environment.")

    dydx_api_credentials = get_dydx_api_credentials(user_id)
    return Client(
        host=host,
        network_id=network_id,
        api_key_credentials=dydx_api_credentials,
    )


async def get_user_account_positions(user_id: str, net: str) -> Dict[str, float]:
    """
    Get the positions in a particular user's account.
    """
    # TODO: optimize by finding a way to do this async
    client = get_dydx_client(user_id, net)
    all_position_data = client.private.get_positions().data["positions"]
    positions = {pos["market"]: float(pos["size"]) for pos in all_position_data}
    return positions


async def get_all_user_account_positions(user_accounts: List[Tuple[str, str]]) -> Dict[str, Dict[str, float]]:
    """
    Gets the positions for each user in a messenger blob.
    """
    user_accounts = list(user_accounts)
    account_positions = await asyncio.gather(
        *[get_user_account_positions(user_id, net) for (user_id, net) in user_accounts]  # list of coroutines
    )
    account_to_positions = {user_accounts[i]: account_positions[i] for i in range(len(user_accounts))}
    return account_to_positions


async def get_user_account_equity(user_id: str, net: str) -> float:
    """
    Get the equity in a particular user's account.
    """
    # TODO: optimize by finding a way to do this async
    client = get_dydx_client(user_id, net)
    user_equity = float(client.private.get_accounts().data["accounts"][0]["equity"])
    return user_equity


async def get_all_user_account_equity(user_accounts: List[Tuple[str, str]]) -> Dict[str, float]:
    """
    Gets the equity for each user in a messenger blob.
    """
    user_accounts = list(user_accounts)
    account_equities = await asyncio.gather(
        *[get_user_account_equity(user_id, net) for (user_id, net) in user_accounts]  # list of coroutines
    )
    account_to_equity = {user_accounts[i]: account_equities[i] for i in range(len(user_accounts))}
    return account_to_equity


async def handle_messaging(
    user_id,
    oracle_prices,
    user_equity,
    user_positions,
    message_platform_config,
    event_trigger_config,
    logger,
):
    """
    * Create an event trigger object from the event trigger config.
    * Check, via builtin method of the trigger object, if the account meets criteria to send message. If it does not meet the criteria, return the empty string. If it does meet the criteria, return the message to be sent.
    * If the message is non-empty, then create a message platform object (via its config). With that object, invoke a "send_message" method.
    """
    message_generator = get_message_generator(event_trigger_config)
    message = message_generator(oracle_prices, user_equity, user_positions)
    if message:
        # get message platform API credentials
        message_platform_name = message_platform_config["message_platform"]
        message_platform_api_key_config_id = message_platform_config[
            "api_key_config_id"
        ]
        message_api_credentials = get_api_credentials(
            user_id, message_platform_name, message_platform_api_key_config_id
        )

        message_platform = get_message_platform(
            message_platform_config, message_api_credentials
        )
        await message_platform.send_message(message, logger)


async def main():
    """
    Entrypoint for running a single iteration of the bot.
    This uses the message configuration to check account
    balances, determine if any positions are in danger of
    liquidation, and send messages.
    """
    logger = get_logger()

    oracle_prices = await OraclePriceGetter.get_all_oracle_prices(logger)

    messenger_blobs = get_messenger_blobs()
    user_accounts = get_all_user_accounts(messenger_blobs) # list of (user_id, network) duples
    (all_positions, all_equity) = await asyncio.gather(
        get_all_user_account_positions(user_accounts), get_all_user_account_equity(user_accounts)
    )

    message_producers = []  # a list of coroutines
    for messenger_blob in messenger_blobs:
        user_id = messenger_blob["user_id"]
        net = messenger_blob["dydx_config"]["environment"]
        account = (user_id, net)
        account_positions = all_positions[account]
        account_equity = all_equity[account]
        message_platform_config = messenger_blob["message_platform_config"]
        event_trigger_config = messenger_blob["event_trigger_config"]
        message_producers.append(
            handle_messaging(
                user_id,
                oracle_prices,
                account_equity,
                account_positions,
                message_platform_config,
                event_trigger_config,
                logger,
            )
        )
    await asyncio.gather(*message_producers)


if __name__ == "__main__":
    asyncio.run(main())