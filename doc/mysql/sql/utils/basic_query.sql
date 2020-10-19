set time_zone = '+13:00';
SELECT @@global.time_zone, @@session.time_zone;
select utc_timestamp();
select now();
select date_format(curdate(), '%d/%m/%Y %H:%i');

select * from company;
select * from location;
select * from raw_rental_route;
select * from rental_route;
select count(*) from rental_route;

select * from daily_quote_scraping_task;
delete from daily_quote_scraping_task t where t.id > 0;

select * from booking_request;
select count(*) from booking_request;
delete from booking_request t where t.id > 0;

select * from rental_quote;

set @debug_enabled = false;
call add_daily_quote_scraping_task(@record_id);
select @record_id;

