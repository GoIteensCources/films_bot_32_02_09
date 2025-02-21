import logging

logger = logging.getLogger(__name__)


def async_log_handlers(func):
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        logger.info(f"Викликано функцію {func.__name__}")
        return result

    return wrapper


@async_log_handlers
def some_handl():
    pass
