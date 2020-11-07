import import_lib

from lib.thrifty.quote import scrape_quotes


def main():
    non_fulfilled_booking_request = {
        "company_id": 1,
        "drop_off_date_value": "11/11/2020",
        "drop_off_office_address": "150 Khyber Pass Road Auckland City, Auckland, 1023",
        "drop_off_office_name": "Auckland City",
        "drop_off_time_value": "01:00 PM",
        "pick_up_date_id": 24,
        "pick_up_date_value": "08/11/2020",
        "pick_up_office_address": "Durey Road Domestic & International Airport Terminal, Christchurch, 8053",
        "pick_up_office_name": "Christchurch Airport",
        "pick_up_time_id": 2,
        "pick_up_time_value": "01:00 PM",
        "rental_duration_id": 4,
        "rental_route_id": 51,
    }
    scrape_quotes(non_fulfilled_booking_request)


if __name__ == "__main__":
    main()