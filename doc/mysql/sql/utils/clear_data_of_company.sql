
-- Step 1: delete rental_quote
delete from rental_quote t where t.id > 0 and t.booking_request_id in (
    select t1.id book_request_id from booking_request t1, booking_request_template t2, rental_route t3, location t4
    where t1.booking_request_template_id = t2.id and t2.rental_route_id = t3.id
    and t3.pick_up_location_id = t4.id and t4.company_id = 2
);

-- Step 1: delete rental_category
delete from rental_category t where t.company_id = 2;

-- Step 2: delete booking_request
delete from booking_request t where t.id > 0 and t.booking_request_template_id in (
    select t1.id book_request_template_id from booking_request_template t1, rental_route t2, location t3
    where t1.rental_route_id = t2.id and t2.pick_up_location_id = t3.id and t3.company_id = 2
);

-- Step: delete booking_request_template
delete from booking_request_template t where t.id > 0 and t.rental_route_id in (
    select t1.id rental_route_id from rental_route t1, location t2
    where t1.pick_up_location_id = t2.id and t2.company_id = 2
);

-- Step: delete rental_route
delete from rental_route t where t.id > 0 and t.pick_up_location_id in (
    select t1.id location_id from location t1
    where t1.company_id = 2
) and t.drop_off_location_id in (
    select t1.id location_id from location t1
    where t1.company_id = 2
);

-- Step: delete location
delete from location t where t.company_id = 2;

-- Step: delete quote_scraping_task
delete from quote_scraping_task t where t.id > 0 and t.id not in
    (select distinct quote_scraping_task_id from booking_request_template);
   
commit;



