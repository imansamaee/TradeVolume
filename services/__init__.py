
import logging

# from services.data.api_data import APIData

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')

file_handler = logging.FileHandler('binance.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)




# API_DATA = APIData("BUSD")
logger.info("API DATA created.")