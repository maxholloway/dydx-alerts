from typing import Dict

# API names
class ApiNames:
    DYDX = "dydx"
    SLACK = "slack"
    EMAIL = "email"

class EventTriggerTypes:
    BELOW_THRESH = "below_thresh"

DEFAULT_DYDX_API_KEY_CONFIG_ID = "0" # there may be more than one set of credentials for each (user, platform) pair; to distinguish between those sets of credentials, we give each set an id. The default ID for dYdX's API credentials is 0, and there is no reason for a user to have more than one credential set for dYdX

class Exchanges:
    BINANCE = "BINANCE"
    BITFINEX = "BITFINEX"
    BITSTAMP = "BITSTAMP"
    BITTREX = "BITTREX"
    COINBASE_PRO = "COINBASE_PRO"
    FTX = "FTX"
    GATE = "GATE"
    GEMINI = "GEMINI"
    HUOBI = "HUOBI"
    KRAKEN = "KRAKEN"
    OKEX = "OKEX"

# TODO: verify that this is right!
PERP_MARKET_TO_SOURCE: Dict = {
    "ETH-USD": [Exchanges.BINANCE, Exchanges.BITSTAMP, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GEMINI, Exchanges.KRAKEN],
    "BTC-USD": [Exchanges.BITSTAMP, Exchanges.BITTREX, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GEMINI, Exchanges.KRAKEN],
    "LINK-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    # "USDT-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.FTX, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "AAVE-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GEMINI, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "UNI-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GEMINI, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "SUSHI-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GATE, Exchanges.HUOBI, Exchanges.OKEX],
    "SOL-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.FTX, Exchanges.HUOBI, Exchanges.OKEX],
    "YFI-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "1INCH-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GATE, Exchanges.GEMINI, Exchanges.HUOBI, Exchanges.OKEX],
    "AVAX-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.GATE, Exchanges.HUOBI, Exchanges.OKEX],
    "SNX-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GEMINI, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "CRV-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GATE, Exchanges.GEMINI, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "UMA-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.GATE, Exchanges.GEMINI, Exchanges.HUOBI, Exchanges.OKEX],
    "DOT-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "DOGE-USD": [Exchanges.BINANCE, Exchanges.FTX, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "MATIC-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.HUOBI, Exchanges.OKEX],
    "MKR-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GATE, Exchanges.HUOBI, Exchanges.OKEX],
    "FIL-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.GEMINI, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "ADA-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.COINBASE_PRO, Exchanges.HUOBI, Exchanges.KRAKEN],
    "ATOM-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "COMP-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "LTC-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "EOS-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.COINBASE_PRO, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "BCH-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.FTX, Exchanges.GEMINI, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "XMR-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "ZEC-USD": [Exchanges.BINANCE, Exchanges.BITFINEX, Exchanges.COINBASE_PRO, Exchanges.GEMINI, Exchanges.HUOBI, Exchanges.KRAKEN, Exchanges.OKEX],
    "ALGO-USD": [Exchanges.BINANCE, Exchanges.COINBASE_PRO, Exchanges.KRAKEN, Exchanges.OKEX],
}

PERP_MARKETS = list(PERP_MARKET_TO_SOURCE.keys())