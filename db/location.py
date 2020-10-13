from db.common import execute_query, execute_transaction


def save_scraped_locations(company_id, scraped_location_names=[]):
    existing_location_names = __get_existing_location_names(company_id)
    new_location_names = __get_new_location_names(
        existing_location_names, scraped_location_names
    )
    if new_location_names:
        __save_new_location_names(company_id, new_location_names)
        __update_rental_routes()


def __get_existing_location_names(company_id):
    def invoke_cursor_func(cursor):
        sql = "select name from location where location.company_id = %s"
        cursor.execute(sql, (company_id,))
        existing_location_names = []
        for (name,) in cursor:
            existing_location_names.append(name)
        return existing_location_names

    return execute_query(invoke_cursor_func)


def __get_new_location_names(existing_location_names=[], scraped_location_names=[]):
    new_location_names = []
    for scraped_location_name in scraped_location_names:
        if scraped_location_name in existing_location_names:
            continue
        new_location_names.append(scraped_location_name)

    return new_location_names


def __save_new_location_names(company_id, new_location_names=[]):
    def invoke_cursor_func(cursor):
        sql = "insert into location(name, company_id) values(%s, %s)"
        new_locations = []
        for new_location_name in new_location_names:
            new_locations.append(
                (
                    new_location_name,
                    company_id,
                )
            )
        cursor.executemany(sql, new_locations)

    execute_transaction(invoke_cursor_func)


def __get_new_rental_routes():
    def invoke_cursor_func(cursor):
        sql = """SELECT
                rrr.pick_up_location_id, rrr.drop_off_location_id
            FROM
                raw_rental_route rrr
            WHERE
                NOT EXISTS( SELECT
                        1
                    FROM
                        rental_route rr
                    WHERE
                        rrr.pick_up_location_id = rr.pick_up_location_id
                            AND rrr.drop_off_location_id = rr.drop_off_location_id)"""
        cursor.execute(sql)
        new_rental_routes = []
        for (
            pick_up_location_id,
            drop_off_location_id,
        ) in cursor:
            new_rental_routes.append(
                (
                    pick_up_location_id,
                    drop_off_location_id,
                )
            )
        return new_rental_routes

    return execute_query(invoke_cursor_func)


def __save_new_rental_routes(new_rental_routes=[]):
    def invoke_cursor_func(cursor):
        sql = "insert into rental_route(pick_up_location_id, drop_off_location_id) values(%s, %s)"
        cursor.executemany(sql, new_rental_routes)

    execute_transaction(invoke_cursor_func)


def __update_rental_routes():
    new_rental_routes = __get_new_rental_routes()
    __save_new_rental_routes(new_rental_routes)
