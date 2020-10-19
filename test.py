from utils.ui import is_empty_string
from budget.location import scrape_locations
from budget.quote import scrape_quotes

scrape_quotes(
    [
        {
            "pick_up_location_input_value": "Auckland Airport, Auckland Ni, New Zealand-(AKL)",
            "pick_up_datetime": "16/10/2020 12:00",
            "drop_off_location_input_value": "63 Arrenway Dr, Unit 6, Auckland Ni, New Zealand-(AK6)",
            "drop_off_datetime": "16/10/2020 12:00",
        }
    ]
)
