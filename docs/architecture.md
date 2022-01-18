# Architecture

## Level 1: Running
This section details how the program will be invoked from the OS.

### Approach 1: Infinite Loop
Have a file called `main.py`. Inside `main.py`, there's the following:
```python
async def main():
    # run everything

if __name__ == "__main__":
    while True:
        await main()
        sleep(5 minutes)
```
To start the bot, just run `python3 main.py`.

### Approach 2: Cron
Same as above, except remove the `while True` and make a cron job that runs the `main()` function once every 5 minutes.

## Level 2: What `main()` does
* Pulls down the index price data for each perp listed on dydx [1 second]. Store in `prices: Dict[perp_name -> price]` dict.
* For each distinct bot user, pulls down their position data [user = distinct stark key]. Store in `user_to_positions: Dict[user->Dict[positions]]` dict.
* For each messenger blob, run the async function `handle_messaging(prices, user_to_positions[messenger_blob[user]])`.
    * Here I define a messenger_blob to be the self-contained config example. This blob has stark public key (i.e. user_id), message platform, api key info, and message config settings (threshold percentage, message frequency, etc). I'm still figuring out if I should put API keys into this config directly. That seems like an insecure way of storing them, however if I don't keep it tightly coupled with the messenger blob, then we'll need some way of accessing the API key data with a key that comes from the messenger blob. Also, you don't want this to be the user's stark key, since a single stark key might have multiple API key configs. This could be accomplished by having a API_KEY_CONFIG_ID that is just an id from 0..infinity, and then (user_id, message_platform, API_KEY_CONFIG_ID) would be a key that maps to {api_key_credentials}. The file with the credentials would need to be encrypted.
* Collect and await all of the open `handle_messaging` tasks.

In code, this looks like the following:
```python

```