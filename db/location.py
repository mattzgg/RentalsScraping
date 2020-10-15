from db.common import execute_query, execute_transaction


def save_locations(company_id, locations=[]):
    def invoke_cursor_func(cursor):
        for location in locations:
            name = location["name"]
            input_value = location["input_value"]
            args = [name, input_value, company_id, 0]
            cursor.callproc("add_rental_location", args)

    execute_transaction(invoke_cursor_func)

    update_rental_routes()


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


def update_rental_routes():
    new_rental_routes = __get_new_rental_routes()
    __save_new_rental_routes(new_rental_routes)