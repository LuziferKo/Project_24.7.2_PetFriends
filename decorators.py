import functools
import logging

logging.basicConfig(filename='log.txt', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def api_request_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("API Requests")
        logger.info(f'Sending API request to {func.__name__}')
        logger.info('URL: {}'.format(args[0]))
        logger.info('Method used: {}'.format(func.__name__))
        logger.info('Arguments: {}'.format(args[1:]))
        logger.info('Keyword arguments: {}'.format(kwargs))

        result = func(*args, **kwargs)

        logger.info(f'Received response from {func.__name__}')
        logger.info('Status Code: {}'.format(result[0]))
        logger.info('Response Body: {}'.format(result[1]))
        return result
    return wrapper