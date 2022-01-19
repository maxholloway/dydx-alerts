# API names
class ApiNames:
    DYDX = "dydx"
    SLACK = "slack"
    EMAIL = "email"

class EventTriggerTypes:
    BELOW_THRESH = "below_thresh"

DEFAULT_DYDX_API_KEY_CONFIG_ID = "0" # there may be more than one set of credentials for each (user, platform) pair; to distinguish between those sets of credentials, we give each set an id. The default ID for dYdX's API credentials is 0, and there is no reason for a user to have more than one credential set for dYdX

PERP_MARKETS = [
    "BTC-USD",
    "ETH-USD",
    "MATIC-USD"
]