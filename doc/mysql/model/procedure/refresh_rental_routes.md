```sql
CREATE PROCEDURE `refresh_rental_routes` ()
BEGIN
	DECLARE _pick_up_location_id INT;
    DECLARE _drop_off_location_id INT;
	DECLARE _done INT DEFAULT FALSE;
	DECLARE new_rental_routes_cursor CURSOR FOR
		SELECT
			pick_up_location.id pick_up_location_id,
			drop_off_location.id drop_off_location_id
		FROM
			location pick_up_location,
			location drop_off_location
		WHERE
			NOT EXISTS( SELECT
					id
				FROM
					rental_route t
				WHERE
					t.pick_up_location_id = pick_up_location_id
						AND t.drop_off_location_id = drop_off_location_id);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
		BEGIN
			GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @err_no = MYSQL_ERRNO, @err_text = MESSAGE_TEXT;
			SET @full_error = CONCAT("ERROR ", @err_no, " (", @sqlstate, "): ", @err_text);
			CALL debug_msg(@debug_enabled, @full_error);

			ROLLBACK;
		END;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET _done = TRUE;

    START TRANSACTION;

	OPEN new_rental_routes_cursor;
	handle_new_rental_routes_loop: LOOP
		SET _done = FALSE;
        FETCH new_rental_routes_cursor INTO _pick_up_location_id, _drop_off_location_id;
		IF _done THEN
			LEAVE handle_new_rental_routes_loop;
		END IF;
        INSERT INTO rental_route(pick_up_location_id, drop_off_location_id) VALUES(_pick_up_location_id, _drop_off_location_id);
	END LOOP;
    COMMIT;
END
```
