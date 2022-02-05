import asyncio
from datetime import datetime as dt

from run import main

async def run_forever(timeout_seconds, delay_seconds):
    while True:
        start = dt.now().timestamp()
        try:
            await asyncio.wait_for(
                main(),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError as to_error:
            print(f"Asyncio timed out with the following:\n{to_error}.")
        
        elapsed_seconds = dt.now().timestamp() - start
    
        if delay_seconds > elapsed_seconds:
            seconds_remaining = delay_seconds-elapsed_seconds
            print(f"Bot run completed. Sleeping for {seconds_remaining} seconds.")
            await asyncio.sleep(seconds_remaining)
        

if __name__ == "__main__":
    # TODO: potentially move these variables into command-line arguments
    five_minute_seconds = 5*60
    ten_minute_seconds = 10*60
    asyncio.run(
        run_forever(timeout_seconds=five_minute_seconds, delay_seconds=ten_minute_seconds)
    )