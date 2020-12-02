import configparser
from mysql import connector
from pathlib import Path

connection_parameters = None


def configure_connection(config_file_name):
    config_file_path = Path(Path(__file__), "..", config_file_name).resolve()
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file_path)
    connection_parameters_section = config_parser["ConnectionParameters"]

    global connection_parameters
    connection_parameters = {
        "host": connection_parameters_section.get("host"),
        "database": connection_parameters_section.get("database"),
        "user": connection_parameters_section.get("user"),
        "password": connection_parameters_section.get("password"),
        "time_zone": connection_parameters_section.get("time_zone"),
    }


def get_db_connection(autocommit=True):
    cnx = connector.connect(**connection_parameters)
    cnx.autocommit = autocommit
    return cnx


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