import pprint


class QuotesNotAvailableException(Exception):
    def __init__(self, scraping_request):
        self.scraping_request = scraping_request

    def __str__(self):
        return (
            "Quotes are not available for the following scraping request: \n{}".format(
                pprint.pformat(self.scraping_request)
            )
        )
