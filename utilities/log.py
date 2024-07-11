import logging

"""Simple logging mechanism."""

LOGGER = logging.getLogger()

def setupLogger():
    ## Configure Logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.INFO)
