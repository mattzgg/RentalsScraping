set time_zone = '+13:00';
SELECT @@global.time_zone, @@session.time_zone;
select utc_timestamp();
select now();
select date_format(curdate(), '%d/%m/%Y %H:%i');

select * from company;
select * from company limit 0, 1;
select * from location;
select * from raw_rental_route;
select * from rental_route;
select count(*) from rental_route;

select * from daily_quote_scraping_task;
delete from daily_quote_scraping_task t where t.id > 0;
set @debug_enabled = false;
call add_daily_quote_scraping_task(@new_daily_quote_scraping_task_id);
select @new_daily_quote_scraping_task_id;

select * from booking_request;
select count(*) from booking_request;
delete from booking_request t where t.id > 0;

select * from rental_quote;
select distinct booking_request_id from rental_quote;

set @debug_enabled = false;
call add_daily_quote_scraping_task(@record_id);
select @record_id;

set @debug_enabled = true;
call clear_data_of_company(2, true);       
call delete_empty_daily_quote_scraping_tasks();

call get_pending_booking_requests(0, 10);

