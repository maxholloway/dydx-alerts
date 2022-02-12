from abc import ABC, abstractmethod
import aiohttp
from aiolimiter import AsyncLimiter
import asyncio
import json
from statistics import median

import ccxt.async_support as ccxt

from constants import Exchanges
from log import get_logger

# Base Clients
class BaseClient(ABC):
    """
    Base exchange client class that all exchange clients should implement.
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def get_index_price(self, market: str) -> float:
        pass

    async def close(self):
        """
        The interface of this client should include this function
        so that we can clean up the client when finished. This is
        meant to be overridden in child classes when necessary, for
        instance when closing a ccxt client.
        """
        return await asyncio.sleep(0)

class CcxtBaseClient(BaseClient):
    def __init__(self, exchange_name):
        self.logger = get_logger()
        if exchange_name == Exchanges.BINANCE: 
            self.client = ccxt.binance({"enableRateLimit": True})
        elif exchange_name == Exchanges.BITFINEX: 
            self.client = ccxt.bitfinex({"enableRateLimit": True})
        elif exchange_name == Exchanges.BITSTAMP: 
            self.client = ccxt.bitstamp({"enableRateLimit": True})
        elif exchange_name == Exchanges.BITTREX: 
            self.client = ccxt.bittrex({"enableRateLimit": True})
        elif exchange_name == Exchanges.COINBASE_PRO: 
            self.client = ccxt.coinbasepro({"enableRateLimit": True})
        elif exchange_name == Exchanges.FTX: 
            self.client = ccxt.ftx({"enableRateLimit": True})
        elif exchange_name == Exchanges.GATE: 
            self.client = ccxt.gateio({"enableRateLimit": True})
        elif exchange_name == Exchanges.GEMINI: 
            self.client = ccxt.gemini({"enableRateLimit": True})
        elif exchange_name == Exchanges.HUOBI:
            self.client = ccxt.huobi({"enableRateLimit": True})
        elif exchange_name == Exchanges.KRAKEN: 
            self.client = ccxt.kraken({"enableRateLimit": True})
        elif exchange_name == Exchanges.OKEX: 
            self.client = ccxt.okex5({"enableRateLimit": True})
        else:
            raise ValueError("Invalid exchange.")

    async def get_index_price(self, market: str) -> float:
        try:
            data = await self.client.fetch_ticker(market)

            price_points = list(filter(
                lambda x: x != None,
                [data["bid"], data["ask"], data["last"]]
            ))
            return median(price_points)
        except Exception as ex:
            print("Exception index price")
            self.logger.error(f"Exception occurred when getting index price. Skipping it and returning -1.\n{ex}", exc_info=True)
            return -1

    async def close(self):
        return await self.client.close()

class ManualClient(BaseClient):
    """
    Client class that makes manual requests to the exchange.
    This requires rate-limiting.

    All child classes must implement `get_index_price_no_rate_limit`, which
    can make an arbitrarily large number of aiohttp calls.
    """
    def __init__(self, requests_per_interval: float, interval_len: float):
        """
        requests_per_interval: number of requests that can occur in a given time interval
        interval_len: number of seconds the rate limit applies

        for example, requests_per_interval=20 interval_len=2 would mean we can make 20 requests per 2 seconds
        """
        self.logger = get_logger()
        self.rate_limiter = AsyncLimiter(requests_per_interval, interval_len)

    async def get_index_price(self, market: str) -> float:
        try:
            index_price = None
            async with self.rate_limiter:
                index_price = await self.get_index_price_no_rate_limit(market)
            return index_price
        except Exception as ex:
            print("Exception index price")
            self.logger.error(f"Exception occurred when getting index price. Skipping it and returning -1.\n{ex}", exc_info=True)
            return -1

    @abstractmethod
    async def get_index_price_no_rate_limit(self, market: str) -> float:
        pass

# Exchange Clients
class BinanceClient(CcxtBaseClient):
    def __init__(self):
        super(BinanceClient, self).__init__(Exchanges.BINANCE)

class BitFinexClient(CcxtBaseClient):
    def __init__(self):
        super(BitFinexClient, self).__init__(Exchanges.BITFINEX)

class BitStampClient(CcxtBaseClient):
    def __init__(self):
        super(BitStampClient, self).__init__(Exchanges.BITSTAMP)

class BitTrexClient(CcxtBaseClient):
    def __init__(self):
        super(BitTrexClient, self).__init__(Exchanges.BITTREX)

class CoinbaseProClient(CcxtBaseClient):
    def __init__(self):
        super(CoinbaseProClient, self).__init__(Exchanges.COINBASE_PRO)

class FtxClient(CcxtBaseClient):
    def __init__(self):
        super(FtxClient, self).__init__(Exchanges.FTX)

class GateClient(CcxtBaseClient):
    def __init__(self):
        super(GateClient, self).__init__(Exchanges.GATE)

class GeminiClient(CcxtBaseClient):
    def __init__(self):
        super(GeminiClient, self).__init__(Exchanges.GEMINI)

class HuobiClient(CcxtBaseClient):
    def __init__(self):
        super(HuobiClient, self).__init__(Exchanges.HUOBI)

class KrakenClient(CcxtBaseClient):
    def __init__(self):
        super(KrakenClient, self).__init__(Exchanges.KRAKEN)

class OkexClient(ManualClient):
    def __init__(self):
        super(OkexClient, self).__init__(10, 2) # should allow 20 requests / 2 seconds, but the okex api sucks and it over-flags on the rate limit

    async def get_index_price_no_rate_limit(self, market: str) -> float:
        base, quote = market.split("/")

        index_price = None
        request_url = f"https://www.okex.com/api/v5/market/ticker?instId={base}-{quote}-SWAP"
        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as resp:
                if resp.status != 200:
                    return -1
                
                resp_dict = json.loads(await resp.text())
                pair_data = resp_dict["data"][0]
                index_price_inputs = pair_data["bidPx"], pair_data["askPx"], pair_data["last"]
                index_price_inputs = [float(p) for p in index_price_inputs]
                index_price = median(index_price_inputs)
        return index_price

if __name__ == "__main__":
    async def tst():
        coros = []
        client = OkexClient()
        for i in range(100):
            coros.append(client.get_index_price("BTC/USDT"))
        return await asyncio.gather(*coros)
    
    val = asyncio.run(
        tst()
    )

    print(val)