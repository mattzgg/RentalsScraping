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
-   A **Rental Duration** represents the number of rental days.
-   A **Booking Request** is an object which encapsulates a query condtion required to operate on a car rental company's website to get rental quotes. It consists of a company, a pick-up location, a pick-up date, a pick-up time, a drop-off location, a drop-off date and a drop-off time. For a designated date, the pick-up date is the day next to it and its booking requests are definite.
-   A **Fulfilled Booking Request** is a booking request whose corresponding rental quotes have been scraped and saved to the database.
-   A **Booking Request Statistics** is an object which reflects the total number of booking requests and the number of fullfilled booking requests for a designated date. The formula to calulcate the total number of booking requests for a designated date is: **<font color="blue">Number of rental routes \* Number of pick-up dates \* Number of pick-up times \* Number of rental durations</font>**

## Business rules to follow

-   Three companies of scraping tasks contain different locations in New Zealand, **Thrifty** with 28 locations, **Budget** with 35 and **Gorentals** with 6.
    The integration of the locations reduce the duplication works.

## Constraints

-   The total number of booking requests handled in a day should be limited to **21600**.
-   Only **5** rental durations are available, namely **1 day**, **2 days**, **3 days**, **4 days** and **5 days**.
-   Only **2** pick-up times are available, namely **9:00 AM** and **1:00 PM**.

## How the rental quotes scraping works

![How Rental Quotes Scraping Works](./doc/how_rqs_works.png?raw=true)

## ERD

![ERD](./doc/mysql/model/ERD.png?raw=true)

## Vehicle Category Sort

-   [vehicle_category_sort.xlsx](./doc/vehicle_category_sort.xlsx)

## Database Views

-   [company_rental_route](./doc/mysql/model/view/company_rental_route.md)

## Database Procedures

-   [add_office](./doc/mysql/model/procedure/add_office.md)
-   [debug_msg](./doc/mysql/model/procedure/debug_msg.md)
-   [get_booking_request_statistics](./doc/mysql/model/procedure/get_booking_request_statistics.md)
-   [get_location_name](./doc/mysql/model/procedure/get_location_name.md)
-   [get_non_fulfilled_booking_requests](./doc/mysql/model/procedure/get_non_fulfilled_booking_requests.md)
-   [refresh_rental_routes](./doc/mysql/model/procedure/refresh_rental_routes.md)

## Database Functions

-   [get_vehicle_category_id](./doc/mysql/model/function/get_vehicle_category_id.md)

## SQL statements

-   [create_schema.sql](./doc/mysql/sql/create_schema.sql)
-   [basic_query.sql](./doc/mysql/sql/basic_query.sql)

## Analysis of Number of Booking Requests for a Designated Date

For **Thrifty**, it has **28** locations, namely **784** (28 \* 28) rental routes. There are **7840** (784 \* 1 \* 2 \* 5) booking requests. Each booking request could bring around **10** rental quotes. So the total of rental quotes could be around **78400** (7840 \* 10).

For **Budget**, it has **35** locations, namely **1225** (35 \* 35) rental routes. There are **12250** (729 \* 1 \* 2 \* 5) booking requests. Each booking request could bring around **10** rental quotes. So the total of rental quotes could be around **122500** (12250 \* 10).

For **GO Rentals**, it has **6** locations, namely **36** (6 \* 6) rental routes. There are **360** (36 \* 1 \* 2 \* 5) booking requests. Each booking request could bring around **20** rental quotes. So the total of rental quotes could be around **7200** (360 \* 20).

In summary, we have **3** companies, **2045** (784 + 1225 + 36) rental routes, **20450** (7840 + 12250 + 360) booking requests and collect around **204500** (78400 + 122500 + 7200) rental quotes and **39** locations after integration of **3** companies.

## References

-   https://selenium-python.readthedocs.io/
-   [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   https://dev.mysql.com/doc/connector-python/en/
-   https://www.crummy.com/software/BeautifulSoup/bs4/doc/
-   https://stackoverflow.com/questions/43164411/why-do-we-still-need-parser-like-beautifulsoup-if-we-can-use-selenium
-   Check the timezone of db server: SELECT @@global.time_zone;
-   Set timezone in MySql workbench: set time_zone = '+13:00';
-   [WebDriver click() vs JavaScript click()](https://stackoverflow.com/questions/34562061/webdriver-click-vs-javascript-click)
