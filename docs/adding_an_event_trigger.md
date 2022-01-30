# Adding an Event Trigger

## Overview
Event triggers are functions that can be thought of as account message generators. An event trigger will take `dYdX` account state (e.g. open positions, account equity) and produce a message from that state (e.g. "your account has an X% collateralization ratio and is near the liquidation point").

This repository was developed with a particular event trigger in mind, namely one that calculates account collateral and produces a message if the account is below some user-defined collateralization ratio.

This document serves as a developer's guide for adding an event trigger to the repository.

## Step 0: Fork the repo and create a branch

## Step 1. Write the Event Trigger
* Inside `event_trigger.py`, create a `make_<trigger_name>_thresh_event_trigger(config_options)` function. This function must return a function `<trigger_name>_event_trigger(index_prices: Dict[str, float], user_equity: float, user_positions: Dict[str, float]) -> str`. See `make_below_thresh_event_trigger` for an example.
* Add a clause to the `get_message_generator(event_trigger_config)`. This conditional is what converts the message generator name in `messenger_blobs.json` to the actual message generator.
* Write unit tests. <!-- TODO: create a unit testing framework -->

## Step 2: Update the Documentation
* Add the event trigger name to the `messenger_blobs.schema` file as one of the "trigger" property enum options. Without this step, nobody will be able to use the new trigger's name in their config.
* Add documentation to `event_triggers.md`.

## Step 3: Add the Event Trigger to the CLI
<!-- TODO: Create the CLI. -->

## Step 4: Test (Manually + Unit)
* Test the workflow manually to make sure the CLI works properly.
* Ensure that all unit tests pass

## Step 5: PR to the Main Repo
* Submit a PR!

