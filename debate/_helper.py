import threading
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

def socket_command(function):
    '''Implement Signals for socket command'''
    
    def wrapper(*args, **kwargs):
        LOGGER.info(f'Command received {function}({args}, {kwargs})')
        return function(*args, **kwargs)
    
    return wrapper

def async_function(function):
    '''Execute a decorated function in a new thread'''

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        thread.start()
        return thread
    
    return wrapper
