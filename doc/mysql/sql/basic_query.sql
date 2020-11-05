set time_zone = '+13:00';
SELECT @@global.time_zone, @@session.time_zone;
select utc_timestamp();
select now();
select date_format(curdate(), '%d/%m/%Y %h:%i %p');

select * from company order by id;
select * from company limit 0, 1;
select * from location order by id;
select * from office;
select * from rental_route;
select count(*) from rental_route;
select * from company_rental_route;

select id, value from pick_up_date;
select id, date_format(value, '%d/%m/%Y %h:%i %p') value from pick_up_date;
call get_booking_request_statistics('04/11/2020', @total_count, @fulfilled_count);
select @total_count, @fulfilled_count;

select * from rental_route order by id;
call get_non_fulfilled_booking_requests('03/11/2020', 1000, 1000);

select * from vehicle_category;
select get_vehicle_category_id(3, 'Manual Cars', 'Toyota Corolla Manual', '5 year(s) old');







