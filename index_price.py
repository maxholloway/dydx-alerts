import asyncio
from statistics import median
from typing import Dict

# import ccxt
import ccxt.async_support as ccxt # link against the asynchronous version of ccxt

from constants import PERP_MARKETS

async def get_index_price(exchange_client, market):
    data = await exchange_client.fetch_ticker(market)
    return median([data["bid"], data["ask"], data["last"]])

async def get_btc_index_price():
    clients = [
        ccxt.bitstamp(),
        ccxt.bittrex(),
        ccxt.coinbasepro(),
        ccxt.ftx(),
        ccxt.gemini(),
        ccxt.kraken()
    ]
    prices = await asyncio.gather(*[get_index_price(client, "BTC/USD") for client in clients])
    return median(prices)

async def get_stablecoin_prices():
    # TODO: get the stablecoin prices needed for dYdX
    return

# async def get_index_price(perp_name: str, stable_coin_prices) -> float:
#     """
#     Docs: https://docs.dydx.exchange/?json#index-prices
#     """
#     # TODO: get the index price using the dYdX API
#     await asyncio.sleep(.0001)
#     return 5_000

async def get_all_index_prices() -> Dict[str, float]:
    stablecoin_prices = await get_stablecoin_prices()
    index_prices = await asyncio.gather(
        *[get_index_price(perp_market, stablecoin_prices) for perp_market in PERP_MARKETS]
    )
    market_to_index_price = {PERP_MARKETS[i]: index_prices[i] for i in range(len(PERP_MARKETS))} # TODO: start async task, but don't await it
    return market_to_index_price

class IndexPriceGetter:
    """
    An ephemeral object that wraps some behavior for getting index prices.
    """
    async def __init__(self):
        pass


if __name__ == "__main__":
    asyncio.run(get_btc_index_price())