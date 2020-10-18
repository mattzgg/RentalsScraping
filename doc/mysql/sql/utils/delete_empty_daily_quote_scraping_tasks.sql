delete from scraping_schedule t where t.id > 0 and t.id not in
    (select distinct scraping_schedule_id from booking_request);

commit;