```sql
CREATE FUNCTION `get_vehicle_category_id`(
	_company_id INT,
    _vehicle_category_name VARCHAR(128), -- vehicle category name scraped from website
    _vehicle_category_description VARCHAR(128), -- mandatory if company is GO Rentals
    _vehicle_age_description VARCHAR(32) -- mandatory if company is GO Rentals
) RETURNS INT
DETERMINISTIC
BEGIN
	DECLARE _vehicle_category_id INT;
    DECLARE _universal_vehicle_category_name VARCHAR(128);
    IF _company_id = 1 THEN -- vehicle category name in Thrifty doesn't change
		SET _universal_vehicle_category_name = _vehicle_category_name;
	ELSEIF _company_id = 2 THEN -- vehicle category name in Budget need to be changed in the following way
		IF _vehicle_category_name = 'Economy' THEN
			SET _universal_vehicle_category_name = 'Economy Car';
		ELSEIF _vehicle_category_name = 'Compact' THEN
			SET _universal_vehicle_category_name = 'Compact Auto';
		ELSEIF _vehicle_category_name = 'Intermediate' THEN
			SET _universal_vehicle_category_name = 'Intermediate Car';
		ELSEIF _vehicle_category_name = 'Full Size' THEN
			SET _universal_vehicle_category_name = 'Full Size Car';
		ELSEIF _vehicle_category_name = 'Full Size Elite' THEN
			SET _universal_vehicle_category_name = 'Full Size Elite Car';
		ELSEIF _vehicle_category_name = 'Compact SUV' THEN
			SET _universal_vehicle_category_name = 'Compact SUV 2WD';
		ELSEIF _vehicle_category_name = 'Intermediate SUV' THEN
			SET _universal_vehicle_category_name = 'Intermediate SUV AWD';
		ELSEIF _vehicle_category_name = 'Full Size Hybrid' THEN
			SET _universal_vehicle_category_name = 'Full Size Hybrid Car';
		ELSEIF _vehicle_category_name = 'Full Size SUV' THEN
			SET _universal_vehicle_category_name = 'Fullsize AWD (seats 5-7 passengers)';
		ELSEIF _vehicle_category_name = 'Premium SUV' THEN
			SET _universal_vehicle_category_name = _vehicle_category_name;
		ELSEIF _vehicle_category_name = 'Premium Ute' THEN
			SET _universal_vehicle_category_name = 'Utility Vehicle with towbar';
		ELSEIF _vehicle_category_name = 'Premium Minivan' THEN
			SET _universal_vehicle_category_name = 'Luxury Van';
		ELSEIF _vehicle_category_name = 'Compact Hybrid' THEN
			SET _universal_vehicle_category_name = 'Compact Hybrid Car';
		ELSEIF _vehicle_category_name = 'Standard SUV' THEN
			SET _universal_vehicle_category_name = 'Intermediate SUV 2WD';
		END IF;
	ELSEIF _company_id = 3 then -- vehicle category name in GO Rentals need to be changed in the following way
		IF _vehicle_category_name = 'Small Cars'
			and _vehicle_category_description = 'Toyota Yaris or similar'
            and _vehicle_age_description = '1 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Economy Car';
		ELSEIF _vehicle_category_name = 'Small Cars'
			and _vehicle_category_description = 'Toyota Corolla Hatch'
            and _vehicle_age_description = '1 - 2 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Compact Auto';
		ELSEIF _vehicle_category_name = 'Small Cars'
			and _vehicle_category_description = 'Toyota CHR or similar'
            and _vehicle_age_description = '1 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Compact SUV 2WD';
		ELSEIF _vehicle_category_name = 'Small Cars'
			and _vehicle_category_description = 'Toyota Corolla Hatch'
            and _vehicle_age_description = '3 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Compact Auto[3 year(s) old]';
		ELSEIF _vehicle_category_name = 'Small Cars'
			and _vehicle_category_description = 'Toyota Corolla Hatch'
            and _vehicle_age_description = '4 - 5 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Compact Auto[4 - 5 year(s) old]';
		ELSEIF _vehicle_category_name = 'Large Cars / SUVs'
			and _vehicle_category_description = 'Toyota Corolla Sedan'
            and _vehicle_age_description = '5 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Intermediate Car[5 year(s) old]';
		ELSEIF _vehicle_category_name = 'Large Cars / SUVs'
			and _vehicle_category_description = 'Toyota Corolla Sedan'
            and _vehicle_age_description = '2 - 3 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Intermediate Car[2 - 3 year(s) old]';
		ELSEIF _vehicle_category_name = 'Large Cars / SUVs'
			and _vehicle_category_description = 'Hyundai Tucson or similar'
            and _vehicle_age_description = '1 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Intermediate SUV 2WD';
		ELSEIF _vehicle_category_name = 'Large Cars / SUVs'
			and _vehicle_category_description = 'Toyota Camry Hybrid'
            and _vehicle_age_description = '4 - 5 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Full Size Hybrid Car';
		ELSEIF _vehicle_category_name = '4 Wheel Drives'
			and _vehicle_category_description = 'Toyota Rav4 AWD or similar'
            and _vehicle_age_description = '2 - 3 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Intermediate SUV AWD';
		ELSEIF _vehicle_category_name = '4 Wheel Drives'
			and _vehicle_category_description = 'Mitsubishi Pajero Sport'
            and _vehicle_age_description = '0 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Fullsize AWD (seats 5-7 passengers)';
		ELSEIF _vehicle_category_name = '4 Wheel Drives'
			and _vehicle_category_description = 'Toyota Land Cruiser Prado'
            and _vehicle_age_description = '1 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Premium SUV';
		ELSEIF _vehicle_category_name = '4 Wheel Drives'
			and _vehicle_category_description = 'Toyota Hilux SR5 4X4'
            and _vehicle_age_description = '1 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Utility Vehicle with towbar';
		ELSEIF _vehicle_category_name = 'Van or People Carriers'
			and _vehicle_category_description = 'Hyundai iMax'
            and _vehicle_age_description = '1 - 2 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Luxury Van';
		ELSEIF _vehicle_category_name = 'Van or People Carriers'
			and _vehicle_category_description = 'Toyota Hiace (10 Seater)'
            and _vehicle_age_description = '2 - 4 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Passenger Van[10 Seats]';
		ELSEIF _vehicle_category_name = 'Van or People Carriers'
			and _vehicle_category_description = 'Toyota Hiace (12 Seater)'
            and _vehicle_age_description = '2 - 5 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Passenger Van';
		ELSEIF _vehicle_category_name = 'Van or People Carriers'
			and _vehicle_category_description = 'Luggage Trailer'
            and _vehicle_age_description = '5 - 12 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Luggage Trailer';
		ELSEIF _vehicle_category_name = 'Manual Cars'
			and _vehicle_category_description = 'Toyota Corolla Manual'
            and _vehicle_age_description = '5 year(s) old' THEN
			SET _universal_vehicle_category_name = 'Manual Cars';
		END IF;
    END IF;

	SELECT
		id
	INTO _vehicle_category_id FROM
		vehicle_category
	WHERE
		name = _universal_vehicle_category_name;
	return _vehicle_category_id;
END
```
