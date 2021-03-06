from typing import Dict

from constants import EventTriggerTypes, COLLATERAL_REQUIREMENTS


def get_message_generator(event_trigger_config):
    """
    Given the event trigger config, return the function that can be used to produce a message.

    event_trigger_config: a dict object that corresponds to the 
        `event_trigger_config` attribute of a messenger blob
    """
    if event_trigger_config["trigger"] == EventTriggerTypes.BELOW_THRESH:
        return make_below_thresh_event_trigger(event_trigger_config["trigger_options"])
    else:
        raise Exception(f"Invalid message action {event_trigger_config['trigger']}")


def make_below_thresh_event_trigger(config_options):
    """
    Create a function that generates a "below threshold event" message.
    """
    def below_thresh_event_trigger(
        oracle_prices: Dict[str, float],
        user_equity: float,
        user_positions: Dict[str, float],
    ):
        account_open_interest = 0
        account_margin_requirement = 0

        maintenance_colalteral_ratios = COLLATERAL_REQUIREMENTS["maintenance"]
        for market_name, pos_size in user_positions.items():
            market_open_interest = abs(pos_size) * oracle_prices[market_name]
            account_open_interest += market_open_interest

            collat_ratio_requirement = float(maintenance_colalteral_ratios[market_name])
            account_margin_requirement += (
                market_open_interest * collat_ratio_requirement
            )

        if account_open_interest == 0:
            # never alert when there's no open interest
            return ""

        account_collateral_pct = 100 * (user_equity / account_open_interest)
        trigger_collateral_pct = float(config_options["collateral_trigger_pct"])
        if account_collateral_pct < trigger_collateral_pct:
            approx_liquidation_pct = 100 * (
                account_margin_requirement / account_open_interest
            )
            return f"Account is {account_collateral_pct:.2f}% collateralized and has ${user_equity:,.2f} of equity. It will be liquidated when it goes below approximately {approx_liquidation_pct:.2f}% collateralization."
        else:
            return ""

    return below_thresh_event_trigger
