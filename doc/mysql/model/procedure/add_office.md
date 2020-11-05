```sql
CREATE PROCEDURE `add_office` (
	IN in_company_id INT,
    IN in_name VARCHAR(128),
    IN in_address VARCHAR(256)
)
BEGIN
	DECLARE _location_id INT;
    DECLARE _location_name VARCHAR(128);
    DECLARE _office_id INT;
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @err_no = MYSQL_ERRNO, @err_text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @err_no, " (", @sqlstate, "): ", @err_text);
		CALL debug_msg(@debug_enabled, @full_error);

        ROLLBACK;
    END;
	START TRANSACTION;

	CALL get_location_name(in_name, _location_name);

	SELECT
    id
INTO _location_id FROM
    location
WHERE
    name = _location_name;
    IF _location_id IS NULL THEN
		INSERT INTO location(name) VALUES(_location_name);
		SELECT LAST_INSERT_ID() INTO _location_id;
	END IF;
SELECT
    id
INTO _office_id FROM
    office
WHERE
    company_id = in_company_id
        AND location_id = _location_id;
    IF _office_id IS NULL THEN
		INSERT INTO office(company_id, location_id, name, address) VALUES(in_company_id, _location_id, in_name, in_address);
		SELECT LAST_INSERT_ID() INTO _office_id;
	ELSE
		UPDATE office SET name = in_name, address = in_address WHERE id = _office_id;
	END IF;
	COMMIT;
END;
```
