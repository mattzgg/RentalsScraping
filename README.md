# RentalsScraping

## Project Dependencies

-   selenium==3.141.0

    `pip install selenium`

-   beautifulsoup4==4.9.3

    `pip install beautifulsoup4`

-   mysql-connector-pyton==8.0.21

    `pip install mysql-connector-python`

-   progress==1.5

    `python -m pip install git+https://github.com/verigak/progress.git@ca6310204e397999ac61ad69f8fba6a7fc775069`

-   termcolor==1.1.0

    `pip install termcolor`

## Concepts

-   A **Rental Route** is defined as a pair of locations. One represents the pick-up location and the other represents the drop-off location. Each car rental company offers customers a number of rental routes.
-   A **Rental Duration** represents the number of rental days. Adding a rental duration to a pick-up date results in a drop-off date.
-   When the program starts to run, the **Scraping Date** is the current date and the **Pick-up Date** is the day next to the scraping date. The program keeps running unless it is forced to quit. As time passes, the scraping date is always the current date as time passes. The pick-up date is always the day next to the scraping date.
-   A **Scraping Request** is an object which encapsulates data required to operate on a car rental company's website to get rental quotes. It consists of a company, a pick-up location, a pick-up date, a pick-up time, a drop-off location, a drop-off date and a drop-off time.
-   A **Fulfilled Scraping Request** is a scraping request whose corresponding rental quotes have been scraped and saved to the database.
-   A **Scraping Request Statistics** is an object which reflects the total number of scraping requests and the number of fullfilled scraping requests for a designated scraping date. The formula to calulcate the total number of scraping requests for a designated scraping date is: **<font color="blue">Number of rental routes \* Number of pick-up times \* Number of rental durations</font>**

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
-   [get_non_fulfilled_scraping_requests](./doc/mysql/model/procedure/get_non_fulfilled_scraping_requests.md)
-   [refresh_rental_routes](./doc/mysql/model/procedure/refresh_rental_routes.md)

## Database Functions

-   [get_vehicle_category_id](./doc/mysql/model/function/get_vehicle_category_id.md)

## SQL statements

-   [create_schema.sql](./doc/mysql/sql/create_schema.sql)
-   [basic_query.sql](./doc/mysql/sql/basic_query.sql)

## Analysis of Number of Scraping Requests for a Designated Date

For **Thrifty**, it has **28** locations, namely **784** (28 \* 28) rental routes. There are **7840** (784 \* 2 \* 5) scraping requests. Each scraping request could bring **1** to **10** rental quotes. So the total of rental quotes could be **7840** to **78400** (7840 \* 10).

For **Budget**, it has **35** locations, namely **1225** (35 \* 35) rental routes. There are **12250** (729 \* 2 \* 5) scraping requests. Each scraping request could bring **1** to **10** rental quotes. So the total of rental quotes could be **12250** to **122500** (12250 \* 10).

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
