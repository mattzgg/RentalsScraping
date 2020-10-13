from mysql import connector
from utils import constants


def get_db_connection():
    return connector.connect(**constants.RENTALS_SCRAPING_DB_CONNECTION_CONIFG)


def execute_query(invoke_cursor_func):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        return invoke_cursor_func(cursor)
    except connector.Error as error:
        raise error
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()


def execute_transaction(invoke_cursor_func):
    try:
        cnx = get_db_connection()
        cnx.autocommit = False
        cursor = cnx.cursor()
        result = invoke_cursor_func(cursor)
        cnx.commit()
        return result
    except connector.Error as error:
        cnx.rollback()
        raise error
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()