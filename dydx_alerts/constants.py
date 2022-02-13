from typing import Dict

# API names
class ApiNames:
    """
    Identifiers of some APIs that are used in the `api_credentials.json`.
    """
    DYDX = "dydx"
    SLACK = "slack"
    EMAIL = "email"


class EventTriggerTypes:
    """
    The names of the event triggers that are supported.
    Currently we only support messages for when the account
    collateral dips below a certain threshold.
    """
    BELOW_THRESH = "below_thresh"


# there may be more than one set of credentials for each (user, platform) pair;
# to distinguish between those sets of credentials, we give each set an id.
# The default ID for dYdX's API credentials is 0. In the future, we may want to
# allow users to have more than one set of dYdX API credentials.
DEFAULT_DYDX_API_KEY_CONFIG_ID = 0

# from https://api.dydx.exchange/v3/markets
COLLATERAL_REQUIREMENTS = {"maintenance": {"BTC-USD": "0.03", "SUSHI-USD": "0.05", "AVAX-USD": "0.05", "1INCH-USD": "0.05", "ETH-USD": "0.03", "XMR-USD": "0.05", "COMP-USD": "0.05", "ALGO-USD": "0.05", "BCH-USD": "0.05", "CRV-USD": "0.05", "UNI-USD": "0.05", "MKR-USD": "0.05", "LTC-USD": "0.05", "EOS-USD": "0.05", "DOGE-USD": "0.05", "ATOM-USD": "0.05", "ZRX-USD": "0.05", "SOL-USD": "0.05", "UMA-USD": "0.05", "AAVE-USD": "0.05", "ADA-USD": "0.05", "SNX-USD": "0.05", "FIL-USD": "0.05", "ZEC-USD": "0.05", "YFI-USD": "0.05", "LINK-USD": "0.05", "DOT-USD": "0.05", "MATIC-USD": "0.05"}, "opening": {"BTC-USD": "0.05", "SUSHI-USD": "0.10", "AVAX-USD": "0.10", "1INCH-USD": "0.10", "ETH-USD": "0.05", "XMR-USD": "0.10", "COMP-USD": "0.10", "ALGO-USD": "0.10", "BCH-USD": "0.10", "CRV-USD": "0.10", "UNI-USD": "0.10", "MKR-USD": "0.10", "LTC-USD": "0.10", "EOS-USD": "0.10", "DOGE-USD": "0.10", "ATOM-USD": "0.10", "ZRX-USD": "0.10", "SOL-USD": "0.10", "UMA-USD": "0.10", "AAVE-USD": "0.10", "ADA-USD": "0.10", "SNX-USD": "0.10", "FIL-USD": "0.10", "ZEC-USD": "0.10", "YFI-USD": "0.10", "LINK-USD": "0.10", "DOT-USD": "0.10", "MATIC-USD": "0.10"}}