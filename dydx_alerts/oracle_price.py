import aiohttp
import json
import os

from dydx3.constants import API_HOST_MAINNET

class OraclePriceGetter:
    def __init__(self, logger):
        self.logger = logger

    async def _get_all_oracle_prices(self):
        request_url = os.path.join(API_HOST_MAINNET, "v3", "markets")

        async with aiohttp.ClientSession() as session:
            async with session.get(request_url) as resp:
                if resp.status != 200:
                    self.logger.error("Failed to get oracle prices from dYdX API.")
                    return -1
                
                resp_dict = json.loads(await resp.text())
                markets = resp_dict["markets"]
                oracle_prices = {market_name: float(market_data["oraclePrice"]) for (market_name, market_data) in markets.items()}
                
                self.logger.info(f"Found oracle prices: {oracle_prices}")
                return oracle_prices


    @staticmethod
    async def get_all_oracle_prices(logger):
        oracle_price_getter = OraclePriceGetter(logger)
        return await oracle_price_getter._get_all_oracle_prices()

if __name__ == "__main__":
    import asyncio
    
    from log import get_logger

    logger = get_logger()
    asyncio.run(OraclePriceGetter.get_all_oracle_prices(logger))