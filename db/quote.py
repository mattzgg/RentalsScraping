from mysql.connector import Error as MySqlError
from db.common import get_db_connection
from utils.datatype import convert_tuple_to_dict


def __get_rental_duration_operation(id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    sql = "select id, type, time_gap, array_size, description from rental_duration_operation t where t.id = %s"
    rental_duration_operation = convert_tuple_to_dict(
        cursor.fetchone(sql, (id,)),
        {
            "0": "id",
            "1": "type",
            "2": "time_gap",
            "3": "array_size",
            "4": "description",
        },
    )

    cursor.close()
    cnx.close()
    return rental_duration_operation


def __get_quote_scraping_task(id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    sql = "select id, created_at, created_by, rental_duration_operation_id from quote_scraping_task t where t.id = %s"
    quote_scraping_task = convert_tuple_to_dict(
        cursor.fetchone(sql, (id,)),
        {
            "0": "id",
            "1": "created_at",
            "2": "created_by",
            "3": "rental_duration_operation_id",
        },
    )
    rental_duration_operation_id = quote_scraping_task.pop(
        "rental_duration_operation_id", None
    )
    if rental_duration_operation_id is not None:
        quote_scraping_task[
            "rental_duration_operation"
        ] = __get_rental_duration_operation(rental_duration_operation_id)

    cursor.close()
    cnx.close()
    return quote_scraping_task


def __get_rental_route(id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    sql = """SELECT
                t1.pick_up_location_id,
                t1.drop_off_location_id,
                t2.name pick_up_location_name,
                t3.name drop_off_location_name
            FROM
                rental_route t1,
                location t2,
                location t3
            WHERE
                t1.pick_up_location_id = t2.id
                    AND t1.drop_off_location_id = t3.id and t1.id = %s """
    rental_route = convert_tuple_to_dict(
        cursor.fetchone(sql, (id,)),
        {
            "0": "pick_up_location_id",
            "1": "drop_off_location_id",
            "2": "pick_up_location_name",
            "3": "drop_off_location_name",
        },
    )

    cursor.close()
    cnx.close()
    return rental_route


def __get_rental_duration(id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    sql = "select id, pick_up_datetime, drop_off_datetime from rental_duration t where t.id = %s"
    rental_duration = convert_tuple_to_dict(
        cursor.fetchone(sql, (id,)),
        {"0": "id", "1": "pick_up_datetime", "2": "drop_off_datetime"},
    )

    cursor.close()
    cnx.close()
    return rental_duration


def __get_booking_request_templates(quote_scraping_task_id):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    quote_scraping_task = __get_quote_scraping_task(quote_scraping_task_id)
    sql = "select id, rental_route_id, rental_duration_id from booking_request_template t where t.quote_scraping_task_id = %s"
    booking_request_templates = []
    for (
        id,
        rental_route_id,
        rental_duration_id,
    ) in cursor:
        booking_request_templates.append(
            {
                "id": id,
                "rental_route": __get_rental_route(rental_route_id),
                "rental_duration": __get_rental_duration(rental_duration_id),
                "quote_scraping_task": quote_scraping_task,
            }
        )

    cursor.close()
    cnx.close()
    return booking_request_templates


def __create_booking_requests(quote_scraping_task_id):
    def __create_booking_requests_based_on_template(booking_request_template):
        rental_duration_operation = booking_request_template["quote_scraping_task"][
            "rental_duration_operation"
        ]
        array_size = rental_duration_operation["array_size"]
        index = 0
        booking_requests = []
        while index < array_size:
            booking_requests.append(
                (
                    booking_request_template["id"],
                    index,
                )
            )
            index += 1

        sql = "insert into booking_request(booking_request_template_id, index) value(%s, %s)"
        cursor.executemany(sql, booking_requests)

    try:
        cnx = get_db_connection()
        cnx.autocommit = False
        cursor = cnx.cursor()

        # delete the relevant rental quotes.
        sql = """delete from rental_quote t1 where t1.booking_request_id in (
            select booking_request_id from booking_request t2 where t2.booking_request_template_id in (
                select booking_request_template_id from booking_request_template t3 where t3.quote_scraping_task_id = %s
            )
        )"""
        cursor.execute(sql, (quote_scraping_task_id,))

        # delete the relevant booking requests.
        sql = """delete from booking_request t1 where t1.booking_request_template_id in (
                select booking_request_template_id from booking_request_template t3 where t3.quote_scraping_task_id = %s
            )"""
        cursor.execute(sql, (quote_scraping_task_id,))

        booking_request_templates = __get_booking_request_templates(
            quote_scraping_task_id
        )
        for booking_request_template in booking_request_templates:
            __create_booking_requests_based_on_template(
                cnx, cursor, booking_request_template
            )

        cnx.commit()
    except MySqlError as error:
        cnx.rollback()
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()


def get_rental_duration_operations():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    sql = "select id, type, time_gap, array_size, description from rental_duration_operation"
    cursor.execute(sql)

    rental_duration_operations = []
    for rental_duration_operation in cursor:
        rental_duration_operations.append(
            convert_tuple_to_dict(
                rental_duration_operation,
                {
                    "0": "id",
                    "1": "type",
                    "2": "time_gap",
                    "3": "array_size",
                    "4": "description",
                },
            )
        )

    cursor.close()
    cnx.close()
    return rental_duration_operations


def get_booking_requests_for_quote_scraping(quote_scraping_task_id):
    pass


def save_rental_categroy(rental_category):
    pass


def save_rental_quote(rental_quote):
    pass