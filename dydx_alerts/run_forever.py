import asyncio
from datetime import datetime as dt

from log import get_logger, IMPORTANT_INFO_LEVEL
from run import main

async def run_forever(timeout_seconds, delay_seconds, logger):
    while True:
        print("Starting bot run.")
        # logger.log(IMPORTANT_INFO_LEVEL, "Beginning a bot run iteration.")
        start = dt.now().timestamp()
        try:
            await asyncio.wait_for(
                main(),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError as to_error:
            print("Asyncio time out error.")
            # logger.error(f"Asyncio time out error.", exc_info=True)
        
        elapsed_seconds = dt.now().timestamp() - start
    
        if delay_seconds > elapsed_seconds:
            seconds_remaining = delay_seconds-elapsed_seconds
            print(f"Bot run completed. Sleeping for {seconds_remaining} seconds.")
            # logger.log(IMPORTANT_INFO_LEVEL, f"Bot run completed. Sleeping for {seconds_remaining} seconds.")
            await asyncio.sleep(seconds_remaining)
        

if __name__ == "__main__":
    # TODO: potentially move these variables into command-line arguments
    five_minute_seconds = 5*60
    ten_minute_seconds = 10*60
    logger = get_logger()
    asyncio.run(
        run_forever(timeout_seconds=five_minute_seconds, delay_seconds=ten_minute_seconds, logger=logger)
    )