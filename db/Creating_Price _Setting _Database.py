import mysql.connector

# Create Connection
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "********"
)
print(mydb)

# Define the Cursor
my_cursor = mydb.cursor()

# Select the Database
my_cursor.execute('USE car_rental_price_setting')

# Create tables for the Database
my_cursor.execute('CREATE TABLE company_location (company_id INT,location_id INT NOT NULL)')

my_cursor.execute('CREATE TABLE location (location_id INT AUTO_INCREMENT PRIMARY kEY,\
                   location_name VARCHAR(30) NOT NULL,\
                   city_name VARCHAR(30) NOT NULL,island_name VARCHAR(15) NOT NULL)')

my_cursor.execute('CREATE TABLE web_scraping_task (task_id INT AUTO_INCREMENT PRIMARY KEY,\
                   task_date DATE NOT NULL, start_time TIME, end_time TIME, \
                   task_status VARCHAR(15) NOT NULL, task_description VARCHAR(300), company_id INT)')

my_cursor.execute('CREATE TABLE company (company_id INT AUTO_INCREMENT PRIMARY KEY,\
                  company_name VARCHAR(30) NOT NULL, address VARCHAR(100), \
                  website_address VARCHAR(50) NOT NULL)')

my_cursor.execute('CREATE TABLE car_category (car_category_id INT AUTO_INCREMENT PRIMARY KEY, \
                  car_category_name VARCHAR(50) NOT NULL)')

my_cursor.execute('CREATE TABLE car (model_id INT AUTO_INCREMENT PRIMARY KEY, \
model_name VARCHAR(30) NOT NULL,car_category_id INT NOT NULL,engine_capacity VARCHAR(10),\
seating_capacity VARCHAR(10),transmission_type VARCHAR(10),number_of_door VARCHAR(10),\
number_of_large_bag VARCHAR(10),number_of_small_bag VARCHAR(10), safety_rating VARCHAR(10))')

my_cursor.execute('CREATE TABLE rental_quote (quote_id INT AUTO_INCREMENT PRIMARY KEY, \
quote_date DATE NOT NULL, model_id INT NOT NULL, \
request_id INT NOT NULL, company_id INT NOT NULL, rental_rate INT NOT NULL, \
availability_status VARCHAR(20), price INT NOT NULL)')

my_cursor.execute('CREATE TABLE rental_request(request_id INT AUTO_INCREMENT PRIMARY KEY, \
pick_up_date DATE NOT NULL, pick_up_time TIME NOT NULL, pick_up_location_id INT, \
drop_off_data DATE NOT NULL, drop_off_time TIME NOT NULL, drop_off_location_id INT,task_id INT )')

my_cursor.execute('CREATE TABLE additional_feature (additional_feature_id INT AUTO_INCREMENT PRIMARY KEY, \
model_id INT, vehicle_stability_control VARCHAR(10), abs VARCHAR(10),fuel_consumption VARCHAR(10), \
bluetooth VARCHAR(10), usb VARCHAR(10), fit_snow_chains VARCHAR(10), cruise_control VARCHAR(10), \
engine_type VARCHAR(10))')

# Add foreign keys
my_cursor.execute('ALTER TABLE company_location ADD FOREIGN KEY(company_id) REFERENCES company(company_id)')

my_cursor.execute('ALTER TABLE company_location ADD FOREIGN KEY(location_id) REFERENCES location(location_id)')

my_cursor.execute('ALTER TABLE web_scraping_task ADD FOREIGN KEY(company_id) REFERENCES company(company_id)')

my_cursor.execute('ALTER TABLE car ADD FOREIGN KEY(car_category_id) REFERENCES car_category(car_category_id)')

my_cursor.execute('ALTER TABLE rental_quote ADD FOREIGN KEY(model_id) REFERENCES car(model_id)')

my_cursor.execute('ALTER TABLE rental_quote ADD FOREIGN KEY(request_id) REFERENCES rental_request(request_id)')

my_cursor.execute('ALTER TABLE rental_quote ADD FOREIGN KEY(company_id) REFERENCES company(company_id)')

my_cursor.execute('ALTER TABLE rental_request ADD FOREIGN KEY(pick_up_location_id) REFERENCES \
location(location_id)')

my_cursor.execute('ALTER TABLE rental_request ADD FOREIGN KEY(drop_off_location_id) REFERENCES \
location(location_id)')

my_cursor.execute('ALTER TABLE rental_request ADD FOREIGN KEY(task_id) REFERENCES \
web_scraping_task(task_id)')

my_cursor.execute('ALTER TABLE additional_feature ADD FOREIGN KEY(model_id) REFERENCES \
car(model_id)')