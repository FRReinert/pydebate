import logging

__author__ = 'Fabricio R Reinert'


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger(__name__).addHandler(NullHandler())