drop view if exists booking_request_for_scraping;
CREATE VIEW `booking_request_for_scraping` AS
SELECT 
    t3.id quote_scraping_task_id,
    t1.id,
    t7.name pick_up_location_name,
    t8.name drop_off_location_name,
    CALC_PICK_UP_DATETIME(t6.pick_up_datetime,
            t4.type,
            t1.index_in_array,
            t4.time_gap) pick_up_datetime,
    CALC_DROP_OFF_DATETIME(t6.drop_off_datetime,
            t4.type,
            t1.index_in_array,
            t4.time_gap) drop_off_datetime
FROM
    booking_request t1,
    booking_request_template t2,
    quote_scraping_task t3,
    rental_duration_operation t4,
    rental_route t5,
    rental_duration t6,
    location t7,
    location t8
WHERE
    t1.booking_request_template_id = t2.id
        AND t2.quote_scraping_task_id = t3.id
        AND t3.rental_duration_operation_id = t4.id
        AND t2.rental_route_id = t5.id
        AND t2.rental_duration_id = t6.id
        AND t5.pick_up_location_id = t7.id
        AND t5.drop_off_location_id = t8.id