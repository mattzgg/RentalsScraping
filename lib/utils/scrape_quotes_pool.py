import signal
from multiprocessing.util import Finalize
from . import constants
from .logging_helpers import get_logger
from .exceptions import QuotesNotAvailableException
from ..utils.data_processing import assemble_quotes, format_scraping_request
from .logging_helpers import configure_log_dispatcher
from ..thrifty.quote import scrape_quotes as scrape_quotes_from_thrifty
from ..budget.quote import scrape_quotes as scrape_quotes_from_budget
from ..gorentals.quote import scrape_quotes as scrape_quotes_from_gorentals

driver_manager = None


class DriverManager:
    def __init__(self, driver_creator, scraping_config):
        self.driver = driver_creator(scraping_config)
        self.scraping_config = scraping_config

    def __enter__(self):
        self.driver.maximize_window()
        return self.driver

    def __exit__(self, *args, **kwargs):
        self.driver.quit()


def sqp_initializer(*args):
    """The initializer used by the Scrape Quotes Pool"""
    # Preclude the need for worker processes to even care about KeyboardInterrupt in the first place.
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    global driver_manager
    driver_creator = args[0]
    scraping_config = args[1]
    driver_manager = DriverManager(driver_creator, scraping_config)
    driver_manager.__enter__()
    Finalize(driver_manager, driver_manager.__exit__, exitpriority=16)

    log_queue = args[2]
    configure_log_dispatcher(log_queue)


SCRAPE_QUOTES_FUNCS = dict(
    [
        (
            constants.THRIFTY_COMPANY_ID,
            scrape_quotes_from_thrifty,
        ),
        (
            constants.BUDGET_COMPANY_ID,
            scrape_quotes_from_budget,
        ),
        (
            constants.GORENTALS_COMPANY_ID,
            scrape_quotes_from_gorentals,
        ),
    ]
)


def sqp_worker(*args):
    logger = get_logger(__name__)

    scraping_request = args[0]
    company_id = scraping_request["company_id"]
    scrape_quotes_func = SCRAPE_QUOTES_FUNCS[company_id]
    global driver_manager
    quotes = assemble_quotes(scraping_request, [])
    try:
        quotes = scrape_quotes_func(
            driver_manager.driver, driver_manager.scraping_config, scraping_request
        )
    except QuotesNotAvailableException as qnae:
        logger.info(str(qnae))
    except:
        logger.exception(
            "An exeception occurred when processing the scraping request: {}".format(
                format_scraping_request(scraping_request)
            )
        )
    else:
        logger.info(
            "{} rental quotes are available for the scraping request: {}".format(
                len(quotes), format_scraping_request(scraping_request)
            )
        )
    return quotes
