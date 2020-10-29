-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema MBIS
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema MBIS680_rentals_prices
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `MBIS680_rentals_prices` DEFAULT CHARACTER SET utf8 ;
USE `MBIS680_rentals_prices` ;

-- -----------------------------------------------------
-- Table `MBIS680_rentals_prices`.`company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MBIS680_rentals_prices`.`company` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MBIS680_rentals_prices`.`location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MBIS680_rentals_prices`.`location` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(256) NOT NULL,
  `input_value` VARCHAR(256) NULL COMMENT 'Some website, e.g. Budget, must use another value instead of name as the input of pick-up location and drop-off location.',
  `island` VARCHAR(45) NOT NULL DEFAULT 'north',
  `company_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_location_company_idx` (`company_id` ASC) VISIBLE,
  CONSTRAINT `fk_location_company`
    FOREIGN KEY (`company_id`)
    REFERENCES `MBIS680_rentals_prices`.`company` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MBIS680_rentals_prices`.`vehicle_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MBIS680_rentals_prices`.`vehicle_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `alias` VARCHAR(128) NOT NULL COMMENT 'For example, the category “Economy” has an alias “Group A”',
  `company_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_vehicle_category_company1_idx` (`company_id` ASC) VISIBLE,
  CONSTRAINT `fk_vehicle_category_company1`
    FOREIGN KEY (`company_id`)
    REFERENCES `MBIS680_rentals_prices`.`company` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MBIS680_rentals_prices`.`vehicle_model`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MBIS680_rentals_prices`.`vehicle_model` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(256) NOT NULL,
  `transmission` VARCHAR(16) NOT NULL DEFAULT 'automatic',
  `seats_count` INT NOT NULL DEFAULT 5,
  `large_bags_count` INT NOT NULL,
  `small_bags_count` INT NOT NULL,
  `has_airconditioning` TINYINT NOT NULL DEFAULT 1,
  `doors_count` INT NOT NULL DEFAULT 4,
  `has_usb` TINYINT NOT NULL DEFAULT 1,
  `has_power_steering` TINYINT NOT NULL DEFAULT 1,
  `security_rating` INT NOT NULL,
  `age` INT NOT NULL,
  `engine_size` DECIMAL(2,1) NOT NULL,
  `fuel_type` VARCHAR(16) NOT NULL DEFAULT 'petrol',
  `fuel_consumption_per_100km` DECIMAL(4,2) NOT NULL,
  `vehicle_category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_vehicle_model_vehicle_category1_idx` (`vehicle_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_vehicle_model_vehicle_category1`
    FOREIGN KEY (`vehicle_category_id`)
    REFERENCES `MBIS680_rentals_prices`.`vehicle_category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MBIS680_rentals_prices`.`rental_route`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MBIS680_rentals_prices`.`rental_route` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pick_up_location_id` INT NOT NULL,
  `drop_off_location_id` INT NOT NULL,
  `distance` DECIMAL NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `fk_location_has_location_location2_idx` (`drop_off_location_id` ASC) VISIBLE,
  INDEX `fk_location_has_location_location1_idx` (`pick_up_location_id` ASC) VISIBLE,
  UNIQUE INDEX `unique_rental_route` (`pick_up_location_id` ASC, `drop_off_location_id` ASC) VISIBLE,
  CONSTRAINT `fk_location_has_location_location1`
    FOREIGN KEY (`pick_up_location_id`)
    REFERENCES `MBIS680_rentals_prices`.`location` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_location_has_location_location2`
    FOREIGN KEY (`drop_off_location_id`)
    REFERENCES `MBIS680_rentals_prices`.`location` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MBIS680_rentals_prices`.`daily_quote_scraping_task`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MBIS680_rentals_prices`.`daily_quote_scraping_task` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `scraping_date` DATE NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MBIS680_rentals_prices`.`booking_request`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MBIS680_rentals_prices`.`booking_request` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rental_route_id` INT NOT NULL,
  `pick_up_datetime` DATETIME NOT NULL,
  `drop_off_datetime` DATETIME NOT NULL,
  `is_quote_available` TINYINT NOT NULL DEFAULT 1,
  `daily_quote_scraping_task_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rental_route_has_rental_duration_rental_route1_idx` (`rental_route_id` ASC) VISIBLE,
  INDEX `fk_booking_request_daily_quote_scraping_task1_idx` (`daily_quote_scraping_task_id` ASC) VISIBLE,
  CONSTRAINT `fk_rental_route_has_rental_duration_rental_route1`
    FOREIGN KEY (`rental_route_id`)
    REFERENCES `MBIS680_rentals_prices`.`rental_route` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_booking_request_daily_quote_scraping_task1`
    FOREIGN KEY (`daily_quote_scraping_task_id`)
    REFERENCES `MBIS680_rentals_prices`.`daily_quote_scraping_task` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MBIS680_rentals_prices`.`rental_quote`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MBIS680_rentals_prices`.`rental_quote` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `price` DECIMAL NOT NULL,
  `is_sold_out` TINYINT NOT NULL DEFAULT 0,
  `vehicle_model_id` INT NOT NULL,
  `booking_request_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rental_quote_vehicle_model1_idx` (`vehicle_model_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_booking_request1_idx` (`booking_request_id` ASC) VISIBLE,
  CONSTRAINT `fk_rental_quote_vehicle_model1`
    FOREIGN KEY (`vehicle_model_id`)
    REFERENCES `MBIS680_rentals_prices`.`vehicle_model` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_rental_quote_booking_request1`
    FOREIGN KEY (`booking_request_id`)
    REFERENCES `MBIS680_rentals_prices`.`booking_request` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `MBIS680_rentals_prices` ;

-- -----------------------------------------------------
-- Placeholder table for view `MBIS680_rentals_prices`.`raw_rental_route`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MBIS680_rentals_prices`.`raw_rental_route` (`pick_up_location_id` INT, `drop_off_location_id` INT);

-- -----------------------------------------------------
-- procedure add_rental_location
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `add_rental_location` (
	in name varchar(255),
	in input_value varchar(255),
    in company_id int,
    out record_id int
)
BEGIN
    select t.id into record_id from location t where t.name = name and t.company_id = company_id;
    if record_id is null then
		insert into location(name, input_value, company_id) values(name, input_value, company_id);
        select last_insert_id() into record_id;
	else
		update location t set t.input_value = input_value where t.name = name and t.company_id = company_id;
	end if;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure add_todays_quote_scraping_task
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `add_todays_quote_scraping_task` (
    out record_id int
)
BEGIN
    declare rental_route_id int;
    declare scraping_date date;
    declare pick_up_datetime, drop_off_datetime datetime;
    declare rental_duration_in_days int;
    declare max_rental_duration_in_days int default 10;
    declare date_format_str varchar(16) default '%d/%m/%Y';
    declare time_format_str varchar(16) default '%H:%i'; -- Hour(00..23)
    declare datetime_format_str varchar(32);

    declare done int default false;
    declare rental_route_cursor cursor for select id from rental_route order by id;
    declare continue handler for not found set done = true;
    declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		call debug_msg(@debug_enabled, @full_error);

        rollback;
    end;

    set scraping_date = curdate();
    select t.id into record_id from daily_quote_scraping_task t where DATE(t.scraping_date) = scraping_date;
    if record_id is null then
        start transaction;

        -- first, create a new daily quote scrapint task.
		insert into daily_quote_scraping_task(scraping_date) values(scraping_date);
        select last_insert_id() into record_id;
        call debug_msg(@debug_enabled, concat('A new daily quote scraping task[', record_id, '] has been created.'));

        set datetime_format_str = concat(date_format_str, ' ', time_format_str);
        set pick_up_datetime = str_to_date(concat(date_format(scraping_date, date_format_str), ' 09:00'), datetime_format_str);
        call debug_msg(@debug_enabled, concat('The pick_up_datetime is: ', date_format(pick_up_datetime, datetime_format_str)));

        -- iterate rental routes to create relevant booking requests.
        call debug_msg(@debug_enabled, 'Start to create booking requests for all rental routes.');
        open rental_route_cursor;
        handle_rental_route_loop: loop
            set done = false;
            fetch rental_route_cursor into rental_route_id;
            if done then
                call debug_msg(@debug_enabled, 'All rental routes have been handled.');
                leave handle_rental_route_loop;
            end if;

            set rental_duration_in_days = 1;
            extend_rental_duration_loop: loop
                if rental_duration_in_days > max_rental_duration_in_days then
                    call debug_msg(@debug_enabled, concat('The rental route[', rental_route_id, '] has been handled.'));
                    leave extend_rental_duration_loop;
                end if;

                set drop_off_datetime = date_add(pick_up_datetime, interval rental_duration_in_days day);

                insert into booking_request(
                    rental_route_id,
                    pick_up_datetime,
                    drop_off_datetime,
                    daily_quote_scraping_task_id
                ) values (
                    rental_route_id,
                    pick_up_datetime,
                    drop_off_datetime,
                    record_id
                );
                call debug_msg(@debug_enabled, concat(
                    'The booking request whose rental duration starts from ',
                    date_format(pick_up_datetime, datetime_format_str),
                    ' to ',
                    date_format(drop_off_datetime, datetime_format_str),
                    ' has been created for the rental route [',
                    rental_route_id,
                    '].'
                    )
                );

                set rental_duration_in_days = rental_duration_in_days + 1;
            end loop;
        end loop;

        close rental_route_cursor;

        commit;
    else
        call debug_msg(@debug_enabled, concat('The daily quote scraping task[', record_id, '] alrealy exists, nothing changed.'));
	end if;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure debug_msg
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `debug_msg` (
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
-- procedure clear_data_of_company
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `clear_data_of_company` (
in company_id int,
in is_location_data_retained boolean
)
BEGIN
    declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		call debug_msg(@debug_enabled, @full_error);

        rollback;
    end;

    start transaction;

	-- Step 1: delete rental_quote
	delete from rental_quote t where t.id > 0 and t.booking_request_id in (
		select t1.id from booking_request t1, rental_route t2, location t3
		where t1.rental_route_id = t2.id and t2.pick_up_location_id = t3.id and
		t3.company_id = company_id
	);

	-- Step 2: delete vehicle_model
	delete from vehicle_model t where t.id > 0 and t.vehicle_category_id in (
		select t1.id from vehicle_category t1 where t1.company_id = company_id
	);

	-- Step 3: delete vechicle_category
	delete from vehicle_category t where t.company_id = company_id;

	-- Step 4: delete booking_request
	delete from booking_request t where t.id > 0 and t.rental_route_id in (
		select t1.id from rental_route t1, location t2 where t1.pick_up_location_id = t2.id
		and t2.company_id = company_id
	);

	if not is_location_data_retained then
		-- Step 5: delete rental_route
		delete from rental_route t where t.id > 0 and t.pick_up_location_id in (
			select t1.id from location t1 where t1.company_id = company_id
		);

		-- Step 6: delete location
		delete from location t where t.company_id = company_id;
	end if;

	commit;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure delete_empty_daily_quote_scraping_tasks
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `delete_empty_daily_quote_scraping_tasks` ()
BEGIN
delete from daily_quote_scraping_task t where t.id > 0 and t.id not in
    (select distinct daily_quote_scraping_task_id from booking_request);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_todays_pending_booking_requests
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `get_todays_pending_booking_requests` (
    in starting_offset int,
    in page_count int
)
BEGIN
	SELECT
		*
	FROM
		(SELECT
			t4.company_id,
				t1.id booking_request_id,
				t1.rental_route_id,
				t4.name pul_name,
				t5.name dol_name,
				t4.input_value pul_input_value,
				t5.input_value dol_input_value,
				DATE_FORMAT(t1.pick_up_datetime, '%d/%m/%Y') pu_date,
				DATE_FORMAT(t1.pick_up_datetime, '%h:%i %p') pu_time, -- Hour(01..12) AM/PM
				DATE_FORMAT(t1.drop_off_datetime, '%d/%m/%Y') do_date,
				DATE_FORMAT(t1.drop_off_datetime, '%h:%i %p') do_time
		FROM
			booking_request t1, daily_quote_scraping_task t2, rental_route t3, location t4, location t5
		WHERE
			t1.daily_quote_scraping_task_id = t2.id
				AND t2.scraping_date = CURDATE()
				AND t1.is_quote_available = TRUE
				AND NOT EXISTS( SELECT
					booking_request_id
				FROM
					rental_quote
				WHERE
					rental_quote.booking_request_id = t1.id)
				AND t1.rental_route_id = t3.id
				AND t3.pick_up_location_id = t4.id
				AND t3.drop_off_location_id = t5.id
		ORDER BY t4.company_id , t1.id , rental_route_id , t1.pick_up_datetime) pending_booking_request
	LIMIT starting_offset , page_count;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure get_todays_booking_request_statistics
-- -----------------------------------------------------

DELIMITER $$
USE `MBIS680_rentals_prices`$$
CREATE PROCEDURE `get_todays_booking_request_statistics` (
	out total int,
    out pending_count int
)
BEGIN
	SELECT
		COUNT(*) into total
	FROM
		booking_request t1,
		daily_quote_scraping_task t2
	WHERE
		t1.daily_quote_scraping_task_id = t2.id
			AND t2.scraping_date = CURDATE();

	SELECT
		COUNT(*) into pending_count
	FROM
		booking_request t1,
		daily_quote_scraping_task t2
	WHERE
		t1.daily_quote_scraping_task_id = t2.id
			AND t2.scraping_date = CURDATE()
			AND t1.is_quote_available = TRUE
			AND NOT EXISTS( SELECT
				*
			FROM
				rental_quote
			WHERE
				rental_quote.booking_request_id = t1.id);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- View `MBIS680_rentals_prices`.`raw_rental_route`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `MBIS680_rentals_prices`.`raw_rental_route`;
USE `MBIS680_rentals_prices`;
CREATE  OR REPLACE VIEW `raw_rental_route` AS
SELECT
    pul.id pick_up_location_id, dol.id drop_off_location_id
FROM
    (SELECT
        id, company_id
    FROM
        location) pul,
    (SELECT
        id, company_id
    FROM
        location) dol
WHERE
    pul.company_id = dol.company_id;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
-- begin attached script 'script'
insert into company(id, name) values(1, 'Thrifty');
insert into company(id, name) values(2, 'Budget');
insert into company(id, name) values(3, 'GO Rentals');
commit;
-- end attached script 'script'
