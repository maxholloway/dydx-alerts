from abc import ABC, abstractmethod
import aiohttp
from aiolimiter import AsyncLimiter
import asyncio
import json
from statistics import median

import ccxt.async_support as ccxt

from constants import Exchanges

class BaseClient(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def get_index_price(self, market: str) -> float:
        pass

    async def close(self):
        return await asyncio.sleep(0)

class CcxtBaseClient:
    def __init__(self, exchange_name):
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
        data = await self.client.fetch_ticker(market)

        price_points = list(filter(
            lambda x: x != None,
            [data["bid"], data["ask"], data["last"]]
        ))
        return median(price_points)

    async def close(self):
        return await self.client.close()
    
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

class OkexClient(BaseClient):
    def __init__(self):
        self.rate_limiter = AsyncLimiter(10, 2) # should allow 20 / 2, but the okex api sucks and it over-flags on the rate limit

    async def get_index_price(self, market: str) -> float:
        base, quote = market.split("/")

        index_price = None
        request_url = f"https://www.okex.com/api/v5/market/ticker?instId={base}-{quote}-SWAP"
        async with aiohttp.ClientSession() as session:
            async with self.rate_limiter:
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
        for i in range(30):
            coros.append(client.get_index_price("BTC/USDT"))
        return await asyncio.gather(*coros)
    
    val = asyncio.run(
        tst()
    )

    print(val)