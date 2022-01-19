import asyncio
from operator import index
from statistics import median
from typing import Dict

import ccxt.async_support as ccxt

from constants import PERP_MARKETS, PERP_MARKET_TO_SOURCE, Exchanges

def tuple_list_to_dict(tuple_list):
    return {k: v for (k, v) in tuple_list}

class IndexPriceGetter:
    """
    An ephemeral object that wraps some behavior for getting index prices.
    """
    def __init__(self):
        self.clients = {
            Exchanges.BINANCE: ccxt.binance({"enableRateLimit": True}),
            Exchanges.BITFINEX: ccxt.bitfinex({"enableRateLimit": True}),
            Exchanges.BITSTAMP: ccxt.bitstamp({"enableRateLimit": True}),
            Exchanges.BITTREX: ccxt.bittrex({"enableRateLimit": True}),
            Exchanges.COINBASE_PRO: ccxt.coinbasepro({"enableRateLimit": True}),
            Exchanges.FTX: ccxt.ftx({"enableRateLimit": True}),
            Exchanges.GATE: ccxt.gateio({"enableRateLimit": True}),
            Exchanges.GEMINI: ccxt.gemini({"enableRateLimit": True}),
            Exchanges.HUOBI: ccxt.huobi(),
            Exchanges.KRAKEN: ccxt.kraken({"enableRateLimit": True}),
            Exchanges.OKEX: ccxt.okex({"enableRateLimit": True}),
        }

    async def cleanup(self):
        await asyncio.gather(*[client.close() for client in self.clients.values()])

    def _get_client(self, exchange_name):
        return self.clients[exchange_name]

    async def _get_index_price_single_exchange(self, exchange_name, market):
        client = self._get_client(exchange_name)
        data = await client.fetch_ticker(market)

        price_points = list(filter(
            lambda x: x != None,
            [data["bid"], data["ask"], data["last"]]
        ))
        return median(price_points)

    async def _get_index_price_many_exchanges(self, exchange_name_to_market: Dict[str, str], usdt_price=None):
        """Gets the index price of the given assets, given multiple exchange with relevant pairs.

        Args:
            exchange_name_to_market (Dict[str, str]): Mapping from the exchange name to the relevant market on that exchange.
            usdt_price (float, optional): The price of USDT, denominated by US dollars. Defaults to None.

        Raises:
            Exception: 

        Returns:
            float: The median of the USDT-adjusted prices across many exchanges.
        """
        exchange_name_to_market_items_list = list(exchange_name_to_market.items())
        prices = await asyncio.gather(*[
            self._get_index_price_single_exchange(exchange_name, market) for (exchange_name, market) in exchange_name_to_market_items_list
        ])

        for i in range(len(exchange_name_to_market_items_list)):
            (exchange_name, market) = exchange_name_to_market_items_list[i]
            if "USDT" in market:
                if usdt_price:
                    prices[i] = prices[i] * usdt_price
                else:
                    raise Exception(f"Failed to convert USDT market {exchange_name}:{market} since no USDT price was provided.")

        return median(prices)

    async def _get_btc_index_price_no_usdt(self) -> float:
        exchange_name_to_market = {
            Exchanges.BITSTAMP: "BTC/USD",
            Exchanges.BITTREX: "BTC/USD",
            Exchanges.COINBASE_PRO: "BTC/USD",
            Exchanges.FTX: "BTC/USD",
            Exchanges.GEMINI: "BTC/USD",
            Exchanges.KRAKEN: "BTC/USD",
        }
        return await self._get_index_price_many_exchanges(exchange_name_to_market)

    async def _get_eth_index_price_no_usdt(self) -> float:
        exchange_name_to_market = {
            # no binance, since binance is denominated in USDT
            Exchanges.BITSTAMP: "ETH/USD",
            Exchanges.COINBASE_PRO: "ETH/USD",
            Exchanges.FTX: "ETH/USD",
            Exchanges.GEMINI: "ETH/USD",
            Exchanges.KRAKEN: "ETH/USD",
        }
        return await self._get_index_price_many_exchanges(exchange_name_to_market)

    async def _get_usdt_index_price(self, btc_index_price, eth_index_price):
        (binance_btc_usdt, bitfinex_usdt_usd, ftx_eth_usdt, huobi_eth_usdt, kraken_usdt_usd, okex_btc_usdt) = \
            await asyncio.gather(*[
                self._get_index_price_single_exchange(Exchanges.BINANCE, "BTC/USDT"),
                self._get_index_price_single_exchange(Exchanges.BITFINEX, "USDT/USD"),
                self._get_index_price_single_exchange(Exchanges.FTX, "ETH/USDT"),
                self._get_index_price_single_exchange(Exchanges.HUOBI, "ETH/USDT"),
                self._get_index_price_single_exchange(Exchanges.KRAKEN, "USDT/USD"),
                self._get_index_price_single_exchange(Exchanges.OKEX, "BTC/USDT")            
            ])
        usdt_prices = (
            btc_index_price / binance_btc_usdt,
            bitfinex_usdt_usd,
            eth_index_price / ftx_eth_usdt,
            eth_index_price / huobi_eth_usdt,
            kraken_usdt_usd,
            btc_index_price / okex_btc_usdt
        )
        return median(usdt_prices)

    async def _get_all_index_prices(self) -> Dict[str, float]:
        (btc_index_price, eth_index_price) = await asyncio.gather(*[
            self._get_btc_index_price_no_usdt(), self._get_eth_index_price_no_usdt() 
        ])
        print("btc index", btc_index_price, "eth_index", eth_index_price)
        usdt_price = await self._get_usdt_index_price(btc_index_price, eth_index_price)
        print("usdt index", usdt_price)

        index_prices = await asyncio.gather(
            *[self._get_index_price_many_exchanges(
                tuple_list_to_dict(source_info), usdt_price) 
                for source_info in PERP_MARKET_TO_SOURCE.values()]
        )
        print("index prices", index_prices)
        market_to_index_price = {PERP_MARKETS[i]: index_prices[i] for i in range(len(PERP_MARKETS))}
        import json
        print("market to index prices", json.dumps(market_to_index_price))
        return market_to_index_price

    @staticmethod
    async def get_all_index_prices():
        index_price_getter = IndexPriceGetter()
        index_prices = await index_price_getter._get_all_index_prices()
        await index_price_getter.cleanup()
        return index_prices

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.get_event_loop().run_until_complete(IndexPriceGetter.get_all_index_prices())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")