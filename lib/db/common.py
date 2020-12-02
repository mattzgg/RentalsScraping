from mysql import connector


def __connect_to_db(db_connection_parameters):
    return connector.connect(**db_connection_parameters)


def execute_query(db_connection_parameters, invoke_cursor_func):
    cnx = __connect_to_db(db_connection_parameters)
    cursor = cnx.cursor()
    try:
        return invoke_cursor_func(cursor)
    finally:
        cursor.close()
        cnx.close()


def execute_transaction(db_connection_parameters, invoke_cursor_func):
    cnx = __connect_to_db({**db_connection_parameters, "autocommit": False})
    cursor = cnx.cursor()
    try:
        result = invoke_cursor_func(cursor)
        cnx.commit()
        return result
    except:
        cnx.rollback()
        raise
    finally:
        cursor.close()
        cnx.close()