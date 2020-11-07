import import_lib

from lib.thrifty.quote import scrape_quotes


def main():
    non_fulfilled_booking_request = {
        "company_id": 1,
        "drop_off_date_value": "10/11/2020",
        "drop_off_office_address": "5 Andrew McKee Avenue Auckland, Auckland, 2022",
        "drop_off_office_name": "Auckland Airport – Domestic",
        "drop_off_time_value": "09:00 AM",
        "pick_up_date_id": 24,
        "pick_up_date_value": "09/11/2020",
        "pick_up_office_address": "5 Andrew McKee Avenue Auckland, Auckland, 2022",
        "pick_up_office_name": "Auckland Airport – Domestic",
        "pick_up_time_id": 2,
        "pick_up_time_value": "09:00 AM",
        "rental_duration_id": 4,
        "rental_route_id": 51,
    }
    scrape_quotes(non_fulfilled_booking_request)


if __name__ == "__main__":
    main()