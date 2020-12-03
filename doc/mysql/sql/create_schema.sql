-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema MBIS680_rentals_prices
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema MBIS680_rentals_prices
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `MBIS680_rentals_prices` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
USE `MBIS680_rentals_prices` ;

-- -----------------------------------------------------
-- Table `company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `company` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rental_duration`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rental_duration` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `number_of_days` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `numer_of_days_UNIQUE` (`number_of_days` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pick_up_date`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pick_up_date` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `value` DATE NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `value_UNIQUE` (`value` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pick_up_time`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pick_up_time` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `value` TIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `value_UNIQUE` (`value` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `location` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rental_route`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rental_route` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pick_up_location_id` INT NOT NULL,
  `drop_off_location_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rental_route_location1_idx` (`pick_up_location_id` ASC) VISIBLE,
  INDEX `fk_rental_route_location2_idx` (`drop_off_location_id` ASC) VISIBLE,
  UNIQUE INDEX `unique_rental_route` (`pick_up_location_id` ASC, `drop_off_location_id` ASC) VISIBLE,
  CONSTRAINT `fk_rental_route_location1`
    FOREIGN KEY (`pick_up_location_id`)
    REFERENCES `location` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rental_route_location2`
    FOREIGN KEY (`drop_off_location_id`)
    REFERENCES `location` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `vehicle_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vehicle_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `description` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rental_quote`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rental_quote` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_id` INT NOT NULL,
  `rental_route_id` INT NOT NULL,
  `pick_up_date_id` INT NOT NULL,
  `pick_up_time_id` INT NOT NULL,
  `rental_duration_id` INT NOT NULL,
  `vehicle_category_id` INT NULL,
  `price` DECIMAL(10,2) NULL COMMENT 'Null price means the price is N/A',
  `created_on` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rental_quote_company_idx` (`company_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_rental_duration1_idx` (`rental_duration_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_pick_up_date1_idx` (`pick_up_date_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_pick_up_time1_idx` (`pick_up_time_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_rental_route1_idx` (`rental_route_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_vehicle_category1_idx` (`vehicle_category_id` ASC) VISIBLE,
  INDEX `unique_rental_quote_idx` (`company_id` ASC, `rental_route_id` ASC, `pick_up_date_id` ASC, `pick_up_time_id` ASC, `rental_duration_id` ASC, `vehicle_category_id` ASC, `price` ASC, `created_on` ASC) VISIBLE,
  CONSTRAINT `fk_rental_quote_company`
    FOREIGN KEY (`company_id`)
    REFERENCES `company` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rental_quote_rental_duration1`
    FOREIGN KEY (`rental_duration_id`)
    REFERENCES `rental_duration` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rental_quote_pick_up_date1`
    FOREIGN KEY (`pick_up_date_id`)
    REFERENCES `pick_up_date` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rental_quote_pick_up_time1`
    FOREIGN KEY (`pick_up_time_id`)
    REFERENCES `pick_up_time` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rental_quote_rental_route1`
    FOREIGN KEY (`rental_route_id`)
    REFERENCES `rental_route` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rental_quote_vehicle_category1`
    FOREIGN KEY (`vehicle_category_id`)
    REFERENCES `vehicle_category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `office`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `office` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_id` INT NOT NULL,
  `location_id` INT NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `address` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_office_company1_idx` (`company_id` ASC) VISIBLE,
  INDEX `fk_office_location1_idx` (`location_id` ASC) VISIBLE,
  CONSTRAINT `fk_office_company1`
    FOREIGN KEY (`company_id`)
    REFERENCES `company` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_office_location1`
    FOREIGN KEY (`location_id`)
    REFERENCES `location` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `MBIS680_rentals_prices` ;

-- -----------------------------------------------------
-- Placeholder table for view `company_rental_route`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `company_rental_route` (`company_id` INT, `rental_route_id` INT, `pick_up_office_id` INT, `pick_up_office_name` INT, `pick_up_office_address` INT, `pick_up_location_id` INT, `pick_up_location_name` INT, `drop_off_office_id` INT, `drop_off_office_name` INT, `drop_off_office_address` INT, `drop_off_location_id` INT, `drop_off_location_name` INT);

-- -----------------------------------------------------
-- procedure debug_msg
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `debug_msg`(
in enabled int,
in msg varchar(255)
)
BEGIN
	if enabled then
		select concat('** ', msg) as '** DEBUG:';
	end if;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure add_office
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
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
END;$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure refresh_rental_routes
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
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
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_location_name
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `get_location_name` (
	in in_office_name varchar(128),
    out out_location_name varchar(128)
)
BEGIN
    IF in_office_name = 'Auckland Airport – Domestic' THEN
        SET out_location_name = 'Auckland Airport';
    ELSEIF in_office_name = 'Picton Ferry Wharf' or in_office_name = 'Picton Ferry Terminal' THEN
        SET out_location_name = 'Picton Ferry';
    ELSEIF in_office_name = 'Wellington City/Ferry' THEN
        SET out_location_name = 'Wellington City';
    ELSEIF in_office_name = 'Wellington Ferry Terminal' THEN
        SET out_location_name = 'Wellington Ferry';
    ELSE
        SET out_location_name = REPLACE(in_office_name, 'Downtown', 'City');
	END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_scraping_request_statistics
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
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
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_pending_scraping_requests
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `get_pending_scraping_requests` (
	IN in_company_id INT,
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
			t1.company_id = in_company_id AND
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
END$$

DELIMITER ;

-- -----------------------------------------------------
-- function get_vehicle_category_id
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
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
END$$

DELIMITER ;

-- -----------------------------------------------------
-- View `company_rental_route`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `company_rental_route`;
USE `MBIS680_rentals_prices`;
CREATE  OR REPLACE VIEW `company_rental_route` AS
    SELECT
        pick_up_office.company_id,
        rental_route.id rental_route_id,
        pick_up_office.id pick_up_office_id,
        pick_up_office.name pick_up_office_name,
        pick_up_office.address pick_up_office_address,
        pick_up_location.id pick_up_location_id,
        pick_up_location.name pick_up_location_name,
        drop_off_office.id drop_off_office_id,
        drop_off_office.name drop_off_office_name,
        drop_off_office.address drop_off_office_address,
        drop_off_location.id drop_off_location_id,
        drop_off_location.name drop_off_location_name
    FROM
        office pick_up_office,
        office drop_off_office,
        rental_route,
        location pick_up_location,
        location drop_off_location
    WHERE
        pick_up_office.company_id = drop_off_office.company_id
            AND pick_up_office.location_id = rental_route.pick_up_location_id
            AND drop_off_office.location_id = rental_route.drop_off_location_id
            AND rental_route.pick_up_location_id = pick_up_location.id
            AND rental_route.drop_off_location_id = drop_off_location.id;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
-- begin attached script 'script'
-- initialize the company table
insert into company(id, name) values(1, 'Thrifty');
insert into company(id, name) values(2, 'Budget');
insert into company(id, name) values(3, 'GO rentals');
commit;

-- initialze the rental_duration table
insert into rental_duration(id, number_of_days) values(1, 1);
insert into rental_duration(id, number_of_days) values(2, 2);
insert into rental_duration(id, number_of_days) values(3, 3);
insert into rental_duration(id, number_of_days) values(4, 4);
insert into rental_duration(id, number_of_days) values(5, 5);
commit;

-- initialze the pick_up_time table
insert into pick_up_time(id, value) values(1, sec_to_time(10*60*60)); -- 10:00 AM
insert into pick_up_time(id, value) values(2, sec_to_time(14*60*60)); -- 02:00 PM
commit;

-- initialize the vehicle_category table
insert into vehicle_category(id, name, description) values(1, 'Economy Car', 'Toyota Yaris or similar');
insert into vehicle_category(id, name, description) values(2, 'Compact Auto', 'Toyota Corolla, Hyundai Accent or similar');
insert into vehicle_category(id, name, description) values(3, 'Compact SUV 2WD', 'Holden Trax or similar');
insert into vehicle_category(id, name, description) values(4, 'Intermediate SUV AWD', 'Toyota RAV4 or similar');
insert into vehicle_category(id, name, description) values(5, 'Fullsize AWD (seats 5-7 passengers)', 'Hyundai Santa Fe or Similar');
insert into vehicle_category(id, name, description) values(6, 'Passenger Van', 'Toyota Hiace or similar');
insert into vehicle_category(id, name, description) values(7, 'Utility Vehicle with towbar', 'Toyota Hilux with towbar or similar');
insert into vehicle_category(id, name, description) values(8, 'Intermediate SUV 2WD', 'Mitsubishi Eclipse or similar');
insert into vehicle_category(id, name, description) values(9, 'Luxury Van', 'Hyundai iMax');
insert into vehicle_category(id, name, description) values(10, 'Electric Vehicle', 'Hyundai IONIQ with 200km range');
insert into vehicle_category(id, name, description) values(11, 'Intermediate Car', 'Hyundai Elantra or similar');
insert into vehicle_category(id, name, description) values(12, 'Full Size Car', 'Toyota Camry or similar');
insert into vehicle_category(id, name, description) values(13, 'Full Size Elite Car', 'Holden Commodore or similar');
insert into vehicle_category(id, name, description) values(14, 'Full Size Hybrid Car', 'Toyota Camry Hybrid or similar');
insert into vehicle_category(id, name, description) values(15, 'Premium SUV', 'Toyota Prado or similar');
insert into vehicle_category(id, name, description) values(16, 'Compact Auto[3 year(s) old]', 'Toyota Corolla Hatch');
insert into vehicle_category(id, name, description) values(17, 'Compact Auto[4 - 5 year(s) old]', 'Toyota Corolla Hatch');
insert into vehicle_category(id, name, description) values(18, 'Intermediate Car[5 year(s) old]', 'Toyota Corolla Sedan');
insert into vehicle_category(id, name, description) values(19, 'Intermediate Car[2 - 3 year(s) old]', 'Toyota Corolla Sedan');
insert into vehicle_category(id, name, description) values(20, 'Passenger Van[10 Seats]', 'Toyota Hiace (10 Seater)');
insert into vehicle_category(id, name, description) values(21, 'Luggage Trailer', 'Luggage Trailer');
insert into vehicle_category(id, name, description) values(22, 'Manual Cars', 'Toyota Corolla Manual');
insert into vehicle_category(id, name, description) values(23, 'Compact Hybrid Car', 'Toyota Corolla Hybrid or similar');
commit;
-- end attached script 'script'
