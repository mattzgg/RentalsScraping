# RentalsScraping

## Usage

```
usage: scrape-quotes [-h] [--company-ids COMPANY_IDS [COMPANY_IDS ...]]
                     [--wait-element-timeout WAIT_ELEMENT_TIMEOUT]
                     [--dom-ready-timeout DOM_READY_TIMEOUT]
                     [--pool-size POOL_SIZE] [--batch-size BATCH_SIZE]
                     [--cache-capacity CACHE_CAPACITY] [--headless]
                     db_config_file_name

positional arguments:
  db_config_file_name   The database configuration file name. The available
                        names is/are: db_config.aws.ini, db_config.uc.ini

optional arguments:
  -h, --help            show this help message and exit
  --company-ids COMPANY_IDS [COMPANY_IDS ...]
                        A list of car rental company id, defaults to [1, 2,
                        3]. Thrifty: 1, Budget: 2, GO rentals: 3
  --wait-element-timeout WAIT_ELEMENT_TIMEOUT
                        The timeout used by the Selenium explicit waits,
                        defaults to 10 seconds
  --dom-ready-timeout DOM_READY_TIMEOUT
                        The timeout used to wait until the document.readyState
                        becomes complete, defaults to 10 seconds,
  --pool-size POOL_SIZE
                        The number of processes that the pool creates to
                        scrape quotes in parallel, defaults to 8
  --batch-size BATCH_SIZE
                        The number of pending scraping requests retrieved from
                        the database at a time, defaults to 1000
  --cache-capacity CACHE_CAPACITY
                        The maximun number of rental quotes that the cache can
                        accommodate, defaults to 1000
  --headless            Enable to use headless Chrome
```

## Project Dependencies

-   selenium==3.141.0

    `pip install selenium`

-   beautifulsoup4==4.9.3

    `pip install beautifulsoup4`

-   mysql-connector-python==8.0.21

    `pip install mysql-connector-python`

## Concepts

-   A **Rental Route** is defined as a pair of locations. One represents the pick-up location and the other represents the drop-off location. Each car rental company offers customers a number of rental routes.
-   A **Rental Duration** represents the number of rental days. Adding a rental duration to a pick-up date results in a drop-off date.
-   When the program starts to run, the **Scraping Date** is the current date and the **Pick-up Date** is the day next to the scraping date. The program keeps running unless it is forced to quit. As time passes, the scraping date is always the current date as time passes. The pick-up date is always the day next to the scraping date.
-   A **Scraping Request** is an object which encapsulates data required to operate on a car rental company's website to get rental quotes. It consists of a company, a pick-up location, a pick-up date, a pick-up time, a drop-off location, a drop-off date and a drop-off time.
-   A **Processed Scraping Request** is a scraping request whose corresponding rental quotes have been scraped and saved to the database.
-   A **Scraping Request Statistics** is an object which reflects the total number of scraping requests and the number of processed scraping requests for a designated scraping date. The formula to calulcate the total number of scraping requests for a designated scraping date is: **<font color="blue">Number of rental routes \* Number of pick-up times \* Number of rental durations</font>**

## Business rules to follow

-   Three companies of scraping tasks contain different locations in New Zealand, **Thrifty** with 28 locations, **Budget** with 35 and **Gorentals** with 6.
    The integration of the locations reduce the duplication works.

## Preset Configuration

-   Only **5** rental durations are available, namely **1 day**, **2 days**, **3 days**, **4 days** and **5 days**.
-   Only **2** pick-up times are available, namely **10:00 AM** and **02:00 PM**.

## How RentalsScraping works

![How RentalsScraping Works](./doc/how_it_works.png?raw=true)

## ERD

![ERD](./doc/mysql/model/ERD.png?raw=true)

## Vehicle Category Sort

-   [vehicle_category_sort.xlsx](./doc/vehicle_category_sort.xlsx)

## Database Views

-   [company_rental_route](./doc/mysql/model/view/company_rental_route.md)

## Database Procedures

-   [add_office](./doc/mysql/model/procedure/add_office.md)
-   [debug_msg](./doc/mysql/model/procedure/debug_msg.md)
-   [get_scraping_request_statistics](./doc/mysql/model/procedure/get_scraping_request_statistics.md)
-   [get_location_name](./doc/mysql/model/procedure/get_location_name.md)
-   [get_pending_scraping_requests](./doc/mysql/model/procedure/get_pending_scraping_requests.md)
-   [refresh_rental_routes](./doc/mysql/model/procedure/refresh_rental_routes.md)

## Database Functions

-   [get_vehicle_category_id](./doc/mysql/model/function/get_vehicle_category_id.md)

## SQL statements

-   [create_schema.sql](./doc/mysql/sql/create_schema.sql)
-   [basic_query.sql](./doc/mysql/sql/basic_query.sql)

## Analysis of Number of Scraping Requests for a Designated Date

For **Thrifty**, it has **28** locations, namely **784** (28 \* 28) rental routes. There are **7840** (784 \* 2 \* 5) scraping requests. Each scraping request could bring **1** to **10** rental quotes. So the total of rental quotes could be **7840** to **78400** (7840 \* 10).

For **Budget**, it has **35** locations, namely **1225** (35 \* 35) rental routes. There are **12250** (1225 \* 2 \* 5) scraping requests. Each scraping request could bring **1** to **10** rental quotes. So the total of rental quotes could be **12250** to **122500** (12250 \* 10).

For **GO Rentals**, it has **6** locations, namely **36** (6 \* 6) rental routes. There are **360** (36 \* 2 \* 5) scraping requests. Each scraping request could bring around **20** rental quotes. So the total of rental quotes could be **360** to **7200** (360 \* 20).

In summary, we have **3** companies, **2045** (784 + 1225 + 36) rental routes, **20450** (7840 + 12250 + 360) scraping requests and collect **20450** (7840 + 12250 + 360) to **208100** (78400 + 122500 + 7200) rental quotes.

## References

-   https://selenium-python.readthedocs.io/
-   [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   https://dev.mysql.com/doc/connector-python/en/
-   https://www.crummy.com/software/BeautifulSoup/bs4/doc/
-   https://stackoverflow.com/questions/43164411/why-do-we-still-need-parser-like-beautifulsoup-if-we-can-use-selenium
-   Check the timezone of db server: SELECT @@global.time_zone;
-   Set timezone in MySql workbench: set time_zone = '+13:00';
-   [WebDriver click() vs JavaScript click()](https://stackoverflow.com/questions/34562061/webdriver-click-vs-javascript-click)
-   [Selenium WebDriver How to Resolve Stale Element Reference Exception?](https://stackoverflow.com/questions/16166261/selenium-webdriver-how-to-resolve-stale-element-reference-exception)
-   [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/)
-   [Context managers and multiprocessing pools](https://stackoverflow.com/questions/24717468/context-managers-and-multiprocessing-pools)
-   [multiprocessing.Pool: What's the difference between map_async and imap?](https://stackoverflow.com/questions/26520781/multiprocessing-pool-whats-the-difference-between-map-async-and-imap)
-   [In what situation do we need to use 'multiprocessing.Pool.imap_unordered'?](https://stackoverflow.com/questions/19063238/in-what-situation-do-we-need-to-use-multiprocessing-pool-imap-unordered)
-   Add RentalsScraping to /usr/local/bin
    -   `ln -s [The absolute path to bin/scrape_quotes.py] /usr/local/bin/scrape-quotes`
    -   `chmod 755 /usr/local/bin/scrape-quotes`
-   [Logging in Python](https://realpython.com/python-logging/)
-   [Python3: Logging With Multiprocessing](https://medium.com/@jonathonbao/python3-logging-with-multiprocessing-f51f460b8778)
