from typing import Dict

# API names
class ApiNames:
    DYDX = "dydx"
    SLACK = "slack"
    EMAIL = "email"


class EventTriggerTypes:
    BELOW_THRESH = "below_thresh"


DEFAULT_DYDX_API_KEY_CONFIG_ID = 0  # there may be more than one set of credentials for each (user, platform) pair; to distinguish between those sets of credentials, we give each set an id. The default ID for dYdX's API credentials is 0. In the future, we may want to allow users to have more than one set of dYdX API credentials.


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


COLLATERAL_REQUIREMENTS = {
    "maintenance": {"BTC-USD": "0.03", "ETH-USD": "0.03", "MATIC-USD": "0.05"},
    "opening": {"BTC-USD": "0.05", "ETH-USD": "0.05", "MATIC-USD": "0.10"},
}

# TODO: verify that all of this is right!
PERP_MARKET_TO_SOURCE: Dict = {
    "ETH-USD": [
        (Exchanges.BINANCE, "ETH/USDT"),
        (Exchanges.BITSTAMP, "ETH/USD"),
        (Exchanges.COINBASE_PRO, "ETH/USD"),
        (Exchanges.FTX, "ETH/USD"),
        (Exchanges.GEMINI, "ETH/USD"),
        (Exchanges.KRAKEN, "ETH/USD"),
    ],
    "BTC-USD": [
        (Exchanges.BITSTAMP, "BTC/USD"),
        (Exchanges.BITTREX, "BTC/USD"),
        (Exchanges.COINBASE_PRO, "BTC/USD"),
        (Exchanges.FTX, "BTC/USD"),
        (Exchanges.GEMINI, "BTC/USD"),
        (Exchanges.KRAKEN, "BTC/USD"),
    ],
    "LINK-USD": [
        (Exchanges.BINANCE, "LINK/USDT"),
        (Exchanges.COINBASE_PRO, "LINK/USD"),
        (Exchanges.HUOBI, "LINK/USDT"),
        (Exchanges.KRAKEN, "LINK/USD"),
        (Exchanges.OKEX, "LINK/USDT"),
    ],
    "AAVE-USD": [
        (Exchanges.BINANCE, "AAVE/USDT"),
        (Exchanges.COINBASE_PRO, "AAVE/USD"),
        (Exchanges.FTX, "AAVE/USD"),
        (Exchanges.GEMINI, "AAVE/USD"),
        (Exchanges.HUOBI, "AAVE/USDT"),
        (Exchanges.KRAKEN, "AAVE/USD"),
        (Exchanges.OKEX, "AAVE/USDT"),
    ],
    "UNI-USD": [
        (Exchanges.BINANCE, "UNI/USDT"),
        (Exchanges.COINBASE_PRO, "UNI/USD"),
        (Exchanges.FTX, "UNI/USD"),
        (Exchanges.GEMINI, "UNI/USD"),
        (Exchanges.HUOBI, "UNI/USDT"),
        (Exchanges.KRAKEN, "UNI/USD"),
        (Exchanges.OKEX, "UNI/USDT"),
    ],
    "SUSHI-USD": [
        (Exchanges.BINANCE, "SUSHI/USDT"),
        (Exchanges.BITFINEX, "SUSHI/USD"),
        (Exchanges.COINBASE_PRO, "SUSHI/USD"),
        (Exchanges.FTX, "SUSHI/USD"),
        (Exchanges.GATE, "SUSHI/USDT"),
        (Exchanges.HUOBI, "SUSHI/USDT"),
        (Exchanges.OKEX, "SUSHI/USDT"),
    ],
    "SOL-USD": [
        (Exchanges.BINANCE, "SOL/USDT"),
        (Exchanges.BITFINEX, "SOL/USD"),
        (Exchanges.FTX, "SOL/USD"),
        (Exchanges.HUOBI, "SOL/USDT"),
        (Exchanges.OKEX, "SOL/USDT"),
    ],
    "YFI-USD": [
        (Exchanges.BINANCE, "YFI/USDT"),
        (Exchanges.BITFINEX, "YFI/USD"),
        (Exchanges.COINBASE_PRO, "YFI/USD"),
        (Exchanges.FTX, "YFI/USD"),
        (Exchanges.HUOBI, "YFI/USDT"),
        (Exchanges.KRAKEN, "YFI/USD"),
        (Exchanges.OKEX, "YFI/USDT"),
    ],
    "1INCH-USD": [
        (Exchanges.BINANCE, "1INCH/USDT"),
        (Exchanges.COINBASE_PRO, "1INCH/USD"),
        (Exchanges.FTX, "1INCH/USD"),
        (Exchanges.GATE, "1INCH/USDT"),
        (Exchanges.GEMINI, "1INCH/USD"),
        (Exchanges.HUOBI, "1INCH/USDT"),
        (Exchanges.OKEX, "1INCH/USDT"),
    ],
    "AVAX-USD": [
        (Exchanges.BINANCE, "AVAX/USDT"),
        (Exchanges.BITFINEX, "AVAX/USD"),
        (Exchanges.GATE, "AVAX/USDT"),
        (Exchanges.HUOBI, "AVAX/USDT"),
        (Exchanges.OKEX, "AVAX/USDT"),
    ],
    "SNX-USD": [
        (Exchanges.BINANCE, "SNX/USDT"),
        (Exchanges.COINBASE_PRO, "SNX/USD"),
        (Exchanges.FTX, "SNX/USD"),
        (Exchanges.GEMINI, "SNX/USD"),
        (Exchanges.HUOBI, "SNX/USDT"),
        (Exchanges.KRAKEN, "SNX/USD"),
        (Exchanges.OKEX, "SNX/USDT"),
    ],
    "CRV-USD": [
        (Exchanges.BINANCE, "CRV/USDT"),
        (Exchanges.COINBASE_PRO, "CRV/USD"),
        (Exchanges.FTX, "CRV/USD"),
        (Exchanges.GATE, "CRV/USDT"),
        (Exchanges.GEMINI, "CRV/USD"),
        (Exchanges.HUOBI, "CRV/USDT"),
        (Exchanges.KRAKEN, "CRV/USD"),
        (Exchanges.OKEX, "CRV/USDT"),
    ],
    "UMA-USD": [
        (Exchanges.BINANCE, "UMA/USDT"),
        (Exchanges.COINBASE_PRO, "UMA/USD"),
        (Exchanges.GATE, "UMA/USDT"),
        (Exchanges.GEMINI, "UMA/USD"),
        (Exchanges.HUOBI, "UMA/USDT"),
        (Exchanges.OKEX, "UMA/USDT"),
    ],
    "DOT-USD": [
        (Exchanges.BINANCE, "DOT/USDT"),
        (Exchanges.BITFINEX, "DOT/USD"),
        (Exchanges.HUOBI, "DOT/USDT"),
        (Exchanges.KRAKEN, "DOT/USD"),
        (Exchanges.OKEX, "DOT/USDT"),
    ],
    "DOGE-USD": [
        (Exchanges.BINANCE, "DOGE/USDT"),
        (Exchanges.FTX, "DOGE/USD"),
        (Exchanges.HUOBI, "DOGE/USDT"),
        (Exchanges.KRAKEN, "DOGE/USD"),
        (Exchanges.OKEX, "DOGE/USDT"),
    ],
    "MATIC-USD": [
        (Exchanges.BINANCE, "MATIC/USDT"),
        (Exchanges.COINBASE_PRO, "MATIC/USD"),
        (Exchanges.FTX, "MATIC/USD"),
        (Exchanges.HUOBI, "MATIC/USDT"),
        (Exchanges.OKEX, "MATIC/USDT"),
    ],
    "MKR-USD": [
        (Exchanges.BINANCE, "MKR/USDT"),
        (Exchanges.COINBASE_PRO, "MKR/USD"),
        (Exchanges.FTX, "MKR/USD"),
        (Exchanges.GATE, "MKR/USDT"),
        (Exchanges.HUOBI, "MKR/USDT"),
        (Exchanges.OKEX, "MKR/USDT"),
    ],
    "FIL-USD": [
        (Exchanges.BINANCE, "FIL/USDT"),
        (Exchanges.COINBASE_PRO, "FIL/USD"),
        (Exchanges.GEMINI, "FIL/USD"),
        (Exchanges.HUOBI, "FIL/USDT"),
        (Exchanges.KRAKEN, "FIL/USD"),
        (Exchanges.OKEX, "FIL/USDT"),
    ],
    "ADA-USD": [
        (Exchanges.BINANCE, "ADA/USDT"),
        (Exchanges.BITFINEX, "ADA/USD"),
        (Exchanges.COINBASE_PRO, "ADA/USD"),
        (Exchanges.HUOBI, "ADA/USDT"),
        (Exchanges.KRAKEN, "ADA/USD"),
    ],
    "ATOM-USD": [
        (Exchanges.BINANCE, "ATOM/USDT"),
        (Exchanges.COINBASE_PRO, "ATOM/USD"),
        (Exchanges.HUOBI, "ATOM/USDT"),
        (Exchanges.KRAKEN, "ATOM/USD"),
        (Exchanges.OKEX, "ATOM/USDT"),
    ],
    "COMP-USD": [
        (Exchanges.BINANCE, "COMP/USDT"),
        (Exchanges.COINBASE_PRO, "COMP/USD"),
        (Exchanges.FTX, "COMP/USD"),
        (Exchanges.HUOBI, "COMP/USDT"),
        (Exchanges.KRAKEN, "COMP/USD"),
        (Exchanges.OKEX, "COMP/USDT"),
    ],
    "LTC-USD": [
        (Exchanges.BINANCE, "LTC/USDT"),
        (Exchanges.COINBASE_PRO, "LTC/USD"),
        (Exchanges.FTX, "LTC/USD"),
        (Exchanges.HUOBI, "LTC/USDT"),
        (Exchanges.KRAKEN, "LTC/USD"),
        (Exchanges.OKEX, "LTC/USDT"),
    ],
    "EOS-USD": [
        (Exchanges.BINANCE, "EOS/USDT"),
        (Exchanges.BITFINEX, "EOS/USD"),
        (Exchanges.COINBASE_PRO, "EOS/USD"),
        (Exchanges.HUOBI, "EOS/USDT"),
        (Exchanges.KRAKEN, "EOS/USD"),
        (Exchanges.OKEX, "EOS/USDT"),
    ],
    "BCH-USD": [
        (Exchanges.BINANCE, "BCH/USDT"),
        (Exchanges.COINBASE_PRO, "BCH/USD"),
        (Exchanges.FTX, "BCH/USD"),
        (Exchanges.GEMINI, "BCH/USD"),
        (Exchanges.HUOBI, "BCH/USDT"),
        (Exchanges.KRAKEN, "BCH/USD"),
        (Exchanges.OKEX, "BCH/USDT"),
    ],
    "XMR-USD": [
        (Exchanges.BINANCE, "XMR/USDT"),
        (Exchanges.BITFINEX, "XMR/USD"),
        (Exchanges.HUOBI, "XMR/USDT"),
        (Exchanges.KRAKEN, "XMR/USD"),
        (Exchanges.OKEX, "XMR/USDT"),
    ],
    "ZEC-USD": [
        (Exchanges.BINANCE, "ZEC/USDT"),
        (Exchanges.BITFINEX, "ZEC/USD"),
        (Exchanges.COINBASE_PRO, "ZEC/USD"),
        (Exchanges.GEMINI, "ZEC/USD"),
        (Exchanges.HUOBI, "ZEC/USDT"),
        (Exchanges.KRAKEN, "ZEC/USD"),
        (Exchanges.OKEX, "ZEC/USDT"),
    ],
    "ALGO-USD": [
        (Exchanges.BINANCE, "ALGO/USDT"),
        (Exchanges.COINBASE_PRO, "ALGO/USD"),
        (Exchanges.KRAKEN, "ALGO/USD"),
        (Exchanges.OKEX, "ALGO/USDT"),
    ],
}

PERP_MARKETS = list(PERP_MARKET_TO_SOURCE.keys())
