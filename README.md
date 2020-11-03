# RentalsScraping

## Prepare the development environment

-   pip install termcolor
-   pip install mysql-connector-python
-   python -m pip install git+https://github.com/verigak/progress.git@ca6310204e397999ac61ad69f8fba6a7fc775069

## Concepts

-   A **Rental Route** is defined as a pair of locations. One represents the pick-up location and the other represents the drop-off location. Each car rental company offers customers a number of rental routes.
-   A **Rental Duration** represents the number of rental days.
-   A **Booking Request** is an object which encapsulates a query condtion required to operate on a car rental company's website to get rental quotes. It consists of a company, a pick-up location, a pick-up date, a pick-up time, a drop-off location, a drop-off date and a drop-off time. For a designated date, the pick-up date is the day next to it and its booking requests are definite.
-   A **Fulfilled Booking Request** is a booking request whose corresponding rental quotes have been scraped and saved to the database.
-   A **Booking Request Statistics** is an object which reflects the total number of booking requests and the number of fullfilled booking requests for a designated date. The formula to calulcate the total number of booking requests for a designated date is: **<font color="blue">Number of rental routes \* Number of pick-up dates \* Number of pick-up times \* Number of rental durations</font>**

## Constraints

-   The total number of booking requests handled in a day should be limited to **21600**.
-   Only **5** rental durations are available, namely **1 day**, **2 days**, **3 days**, **4 days** and **5 days**.
-   Only **2** pick-up times are available, namely **9:00 AM** and **1:00 PM**.

## How the rental quotes scraping works

![How Rental Quotes Scraping Works](./doc/how_rqs_works.png?raw=true)

## ERD

![ERD](./doc/mysql/model/ERD.png?raw=true)

## The SQL code to create the **company_rental_route** view

```sql
CREATE VIEW `company_rental_route` AS
    SELECT
        pick_up_office.company_id,
        rental_route.id rental_route_id,
        pick_up_office.location_id pick_up_location_id,
        pick_up_loaction.name pick_up_location_name,
        pick_up_office.address pick_up_location_address,
        drop_off_office.location_id drop_off_location_id,
        drop_off_location.name drop_off_location_name,
        drop_off_office.address drop_off_location_address
    FROM
        office pick_up_office,
        office drop_off_office,
        rental_route,
        location pick_up_location,
        location drop_off_location
    WHERE
        pick_up_office.company_id = drop_off_office.company_id
            AND pick_up_office.location_id = rental_route.pick_up_location_id
            AND drop_off_office.location_id = rental_route.drop_off_location_id
            AND rental_route.pick_up_location_id = pick_up_location.id
            AND rental_route.drop_off_location_id = drop_off_location.id
```

## Initialize the DB with company, rental_duration and pick-up times

```sql
-- initialize the company table
insert into company(id, name) values(1, 'Thrifty');
insert into company(id, name) values(2, 'Budget');
insert into company(id, name) values(3, 'GO Rentals');
commit;

-- initialze the rental_duration table
insert into rental_duration(id, number_of_days) values(1, 1);
insert into rental_duration(id, number_of_days) values(2, 2);
insert into rental_duration(id, number_of_days) values(3, 3);
insert into rental_duration(id, number_of_days) values(4, 4);
insert into rental_duration(id, number_of_days) values(5, 5);

-- initialze the pick_up_time table
insert into pick_up_time(id, value) values(1, sec_to_time(9*60*60)); -- 09:00 AM
insert into pick_up_time(id, value) values(2, sec_to_time(13*60*60)); -- 01:00 PM
```

## Initialize the DB with locations and rental routes

## Analysis of Number of Booking Requests for a Designated Date

For **Thrifty**, it has **28** locations, namely **784** (28 \* 28) rental routes. There are **7840** (784 \* 1 \* 2 \* 5) booking requests. Each booking request could bring around **10** rental quotes. So the total of rental quotes could be around **78400** (7840 \* 10).

For **Budget**, it has **35** locations, namely **1225** (35 \* 35) rental routes. There are **12250** (729 \* 1 \* 2 \* 5) booking requests. Each booking request could bring around **10** rental quotes. So the total of rental quotes could be around **122500** (12250 \* 10).

For **GO Rentals**, it has **6** locations, namely **36** (6 \* 6) rental routes. There are **360** (36 \* 1 \* 2 \* 5) booking requests. Each booking request could bring around **20** rental quotes. So the total of rental quotes could be around **7200** (360 \* 20).

In summary, we have **3** companies, **2045** (784 + 1225 + 36) rental routes, **20450** (7840 + 12250 + 360) booking requests and collect around **204500** (78400 + 122500 + 7200) rental quotes.

## References

-   https://selenium-python.readthedocs.io/
-   [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   https://dev.mysql.com/doc/connector-python/en/
-   https://www.crummy.com/software/BeautifulSoup/bs4/doc/
-   https://stackoverflow.com/questions/43164411/why-do-we-still-need-parser-like-beautifulsoup-if-we-can-use-selenium
-   Check the timezone of db server: SELECT @@global.time_zone;
-   Set timezone in MySql workbench: set time_zone = '+13:00';
