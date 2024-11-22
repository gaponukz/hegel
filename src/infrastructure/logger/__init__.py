import functools
import time

from loguru import logger


def log_interactor(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Interactor '{func.__name__}' called")

        try:
            result = await func(*args, **kwargs)
            logger.info(f"Interactor '{func.__name__}' finished without errors")
            return result

        except Exception as e:
            logger.error(
                f"Interactor '{func.__name__}' raised an exception ({e.__class__.__name__}): {e}"
            )
            raise

        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(
                f"Interactor '{func.__name__}' executed in {elapsed_time:.4f} seconds"
            )

    return wrapper
