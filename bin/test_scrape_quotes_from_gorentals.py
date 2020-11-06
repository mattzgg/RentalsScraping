import import_lib

from lib.gorentals.quote import scrape_quotes


def main():
    non_fulfilled_booking_request = {
        "company_id": 3,
        "drop_off_date_value": "11/11/2020",
        "drop_off_office_address": "165 Beach Road, Auckland City, Auckland, 1010",
        "drop_off_office_name": "Auckland City",
        "drop_off_time_value": "01:00 PM",
        "pick_up_date_id": 24,
        "pick_up_date_value": "08/11/2020",
        "pick_up_office_address": "Sir Henry Wigley Drive, Frankton, Queenstown, 9300",
        "pick_up_office_name": "Queenstown Airport",
        "pick_up_time_id": 2,
        "pick_up_time_value": "01:00 PM",
        "rental_duration_id": 4,
        "rental_route_id": 51,
    }
    scrape_quotes(non_fulfilled_booking_request)


if __name__ == "__main__":
    main()