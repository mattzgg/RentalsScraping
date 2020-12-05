from lib.utils.data_processing import format_scraping_request


class QuotesNotAvailableException(Exception):
    def __init__(self, scraping_request):
        self.scraping_request = scraping_request

    def __str__(self):
        return "Rental quotes are not available for the scraping request: {}".format(
            format_scraping_request(self.scraping_request)
        )
