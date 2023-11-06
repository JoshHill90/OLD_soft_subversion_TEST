import logging

logging.basicConfig(
    level=logging.ERROR,
    filename='error.log', 
    format='%(asctime)s [%(levelname)s]: %(message)s',
)