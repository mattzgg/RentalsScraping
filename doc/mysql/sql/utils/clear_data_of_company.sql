
-- Step 1: delete rental_quote
delete from rental_quote t where t.id > 0 and t.booking_request_id in (
    select t1.id from booking_request t1, rental_route t2, location t3
    where t1.rental_route_id = t2.id and t2.pick_up_location_id = t3.id and
    t3.company_id = ?
);

-- Step 2: delete vehicle_model
delete from vehicle_model t where where t.id > 0 and t.vehicle_category_id in (
    select t1.id from vehicle_category t1 where t1.company_id = ?
);

-- Step 3: delete vechicle_category
delete from vehicle_category t where t.company_id = ?

-- Step 4: delete booking_request
delete from booking_request t where t.id > 0 and t.rental_route_id in (
    select r1.id from rental_route t1, location t2 where t1.pick_up_location_id = t2.id
    and t2.company_id = ?
);

-- Step 5: delete rental_route
delete from rental_route t where t.id > 0 and t.pick_up_location_id in (
    select t1.id from location t1 where t1.company_id = ?
);

-- Step 6: delete location
delete from location t where t.company_id = ?;

commit;
