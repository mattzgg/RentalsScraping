```sql
CREATE PROCEDURE `get_pending_scraping_requests` (
	IN in_scraping_date_str VARCHAR(10), -- %d/%m/%Y
    IN in_offset INT,
    IN in_row_count INT
)
BEGIN
	DECLARE _scraping_date DATE;
    DECLARE _pick_up_date DATE;
    DECLARE _pick_up_date_id INT;

    set _scraping_date = str_to_date(in_scraping_date_str, '%d/%m/%Y');
    set _pick_up_date = DATE_ADD(_scraping_date, INTERVAL 1 DAY);

    SELECT id INTO _pick_up_date_id FROM pick_up_date t WHERE t.value = _pick_up_date;
    IF _pick_up_date_id IS NOT NULL THEN
		SELECT
			t1.company_id,
			t1.rental_route_id,
			t2.id pick_up_date_id,
			t3.id pick_up_time_id,
			t4.id rental_duration_id,
			t1.pick_up_office_name,
			t1.pick_up_office_address,
			t1.drop_off_office_name,
			t1.drop_off_office_address,
			DATE_FORMAT(t2.value, '%d/%m/%Y') pick_up_date_value,
			TIME_FORMAT(t3.value, '%h:%i %p') pick_up_time_value,
			DATE_FORMAT(DATE_ADD(t2.value,
						INTERVAL t4.number_of_days DAY),
					'%d/%m/%Y') drop_off_date_value,
			TIME_FORMAT(t3.value, '%h:%i %p') drop_off_time_value
		FROM
			company_rental_route t1,
			pick_up_date t2,
			pick_up_time t3,
			rental_duration t4
		WHERE
			t2.id = _pick_up_date_id AND
			NOT EXISTS( SELECT
					id
				FROM
					rental_quote t5
				WHERE
					t5.company_id = t1.company_id
						AND t5.rental_route_id = t1.rental_route_id
						AND t5.pick_up_date_id = t2.id
						AND t5.pick_up_time_id = t3.id
						AND t5.rental_duration_id = t4.id)
		ORDER BY t1.company_id , t1.rental_route_id , t2.id , t3.id , t4.id
		LIMIT in_offset , in_row_count;
    END IF;
END
```
