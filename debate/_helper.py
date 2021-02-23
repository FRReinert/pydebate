import threading
import logging

def async_function(function):
    '''Execute a decorated function in a new thread'''

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    
    return wrapper


def check_carriage_return(b):
    '''Check if data is a carriage return'''
    return True if b == '\r\n' or b == '\n' else False

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
