# Working Doc

## Milestone 1: Core Module
* [ ] Get a working example with manual config
    * [ x ] Get to an agreeable separation of api credentials and bot config. **Done: putting all credentials into `api_credentials.json`, and rest of config into `messenger_blobs.json`**
    * [ x ] Run an async function from the top-level of a python file
    * [ x ] Re-write all `start(...)` to use a "start and collect" model, where I start a bunch of async tasks and then await the overall result.
    * [ ] Build `get_all_index_prices()`
        * [ ] Build `get_stablecoin_prices()`
        * [ ] Build `get_index_price(perp_market, stablecoin_prices)`
    * [ ] Build `get_all_users_positions(user_ids)`
        * [ ] Build `get_user_positions(user_id)`
    * [ ] Build `get_all_users_equity(user_ids)`
        * [ ] Build `get_user_equity(user_id)`
    * [ ] Build `handle_messaging()`
        * [ ] Build a message constructor that checks collateralization and constructs a message if it's below a threshold. Modify `messenger_blobs.json` to use this event trigger message. This includes building `get_message_generator(event_trigger_config)`.
        * [ ] Build `get_message_platform(message_platform_config)`; build a simple message platform (e.g. 'slack') that implements credential setting and message sending. Modify `messenger_blobs.json` and `api_credentials.json` to use this message platform and its api credentials.
    * [ ] Get a working run with manual config setting.
