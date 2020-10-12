from mysql import connector
from utils import constants


def get_db_connection():
    return connector.connect(**constants.RENTALS_SCRAPING_DB_CONNECTION_CONIFG)