"""
Entrypoint for running the bot.
"""
import asyncio
from datetime import datetime as dt

from log import get_logger, IMPORTANT_INFO_LEVEL
from run import main


async def run_forever(timeout_seconds, delay_seconds, logger):
    """
    Thin wrapper above run.py's `main()` function; just run the `main()`
    on repeat forever.
    """
    while True:
        logger.info("Beginning a bot run iteration.")
        start = dt.now().timestamp()
        try:
            await asyncio.wait_for(main(), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            logger.error("Asyncio time out error.", exc_info=True)

        elapsed_seconds = dt.now().timestamp() - start

        if delay_seconds > elapsed_seconds:
            seconds_remaining = delay_seconds - elapsed_seconds
            logger.info(
                f"Bot run completed after {elapsed_seconds:<.2f} seconds. Sleeping for {seconds_remaining:<.2f} seconds."
            )
            await asyncio.sleep(seconds_remaining)


if __name__ == "__main__":
    # TODO: potentially move these variables into command-line arguments
    FIVE_MINUTES_SECONDS = 5 * 60
    TEN_MINUTES_SECONDS = 10 * 60
    logger = get_logger()
    asyncio.run(
        run_forever(
            timeout_seconds=FIVE_MINUTES_SECONDS,
            delay_seconds=TEN_MINUTES_SECONDS,
            logger=logger,
        )
    )
