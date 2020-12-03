```sql
CREATE PROCEDURE `get_scraping_request_statistics` (
	IN in_company_id INT,
	IN in_scraping_date_str VARCHAR(10), -- %d/%m/%Y
    OUT out_total_count INT,
    OUT out_processed_count INT
)
BEGIN
	DECLARE _scraping_date DATE;
    DECLARE _pick_up_date DATE;
    DECLARE _pick_up_date_id INT;
    DECLARE _company_rental_route_count INT;
    DECLARE _pick_up_time_count INT;
    DECLARE _rental_duration_count INT;

    set _scraping_date = str_to_date(in_scraping_date_str, '%d/%m/%Y');
    set _pick_up_date = DATE_ADD(_scraping_date, INTERVAL 1 DAY);

    SELECT id INTO _pick_up_date_id FROM pick_up_date t WHERE t.value = _pick_up_date;
    IF _pick_up_date_id is null THEN
		INSERT INTO pick_up_date(value) VALUES(_pick_up_date);
        SELECT LAST_INSERT_ID() INTO _pick_up_date_id;
	END IF;

    -- Calculate the total count of scraping requests required for a day.
    SELECT count(*) INTO _company_rental_route_count FROM company_rental_route WHERE company_id = in_company_id;
    SELECT count(*) INTO _pick_up_time_count FROM pick_up_time;
    SELECT count(*) INTO _rental_duration_count FROM rental_duration;
    SET out_total_count = _company_rental_route_count * _pick_up_time_count * _rental_duration_count;

    -- Get the count of processed scraping requests for the designated day.
	SELECT
		COUNT(DISTINCT company_id,
			rental_route_id,
			pick_up_date_id,
			pick_up_time_id,
			rental_duration_id)
	INTO out_processed_count FROM
		rental_quote
	WHERE
		company_id = in_company_id AND
        pick_up_date_id = _pick_up_date_id;
END
```
