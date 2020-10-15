-- Prepare Booking Request Templates
select * from rental_route;
SELECT 
    t1.id,
    t1.pick_up_location_id,
    t1.drop_off_location_id,
    t2.name pick_up_location_name,
    t3.name drop_off_location_name,
    t4.id company_id,
    t4.name company_name
FROM
    rental_route t1,
    location t2,
    location t3,
    company t4
WHERE
    t1.pick_up_location_id = t2.id
        AND t1.drop_off_location_id = t3.id
        AND t3.company_id = t4.id
        AND t2.name LIKE 'Auckland%'
        AND t3.name LIKE 'Auckland%';
        
-- Prepare Rental Duration
select * from rental_duration;
select curdate();
select DATE_FORMAT(curdate(), '%d/%m/%Y %H:%i');
select STR_TO_DATE('15/10/2020 12:00', '%d/%m/%Y %H:%i');

insert into rental_duration(pick_up_datetime, drop_off_datetime) 
	values(str_to_date('15/10/2020 12:00', '%d/%m/%Y %H:%i'), str_to_date('16/10/2020 12:00', '%d/%m/%Y %H:%i'));
commit;


-- Check booking requests        
select * from booking_request_template;
insert into booking_request_template(rental_route_id, rental_duration_id) values(3677, 1);
commit;

select * from booking_request;

select * from quote_scraping_task;




