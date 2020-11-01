-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema rentals_scraping
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema rentals_scraping
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `rentals_scraping` DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ;
USE `rentals_scraping` ;

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
-- Table `vehicle_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vehicle_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `vehicle_model`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vehicle_model` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `vehicle_category_id` INT NOT NULL,
  `name` VARCHAR(256) NOT NULL,
  `age` INT NOT NULL DEFAULT 1,
  `transmission` VARCHAR(16) NOT NULL DEFAULT 'Automatic',
  `engine_size` DECIMAL(2,1) NOT NULL,
  `fuel_type` VARCHAR(16) NOT NULL DEFAULT 'Petrol',
  `fuel_consumption_per_100km` DECIMAL(4,2) NOT NULL,
  `number_of_seats` INT NOT NULL DEFAULT 5,
  `number_of_doors` INT NOT NULL DEFAULT 5,
  `number_of_large_bags` INT NOT NULL DEFAULT 2,
  `number_of_small_bags` INT NOT NULL DEFAULT 2,
  `has_airconditioning` TINYINT NOT NULL DEFAULT 1,
  `has_usb` TINYINT NOT NULL DEFAULT 1,
  `has_power_steering` TINYINT NOT NULL DEFAULT 1,
  `security_rating` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `fk_vehicle_model_vehicle_category1_idx` (`vehicle_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_vehicle_model_vehicle_category1`
    FOREIGN KEY (`vehicle_category_id`)
    REFERENCES `vehicle_category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
-- Table `rental_quote`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rental_quote` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_id` INT NOT NULL,
  `rental_route_id` INT NOT NULL,
  `pick_up_date_id` INT NOT NULL,
  `pick_up_time_id` INT NOT NULL,
  `rental_duration_id` INT NOT NULL,
  `vehicle_model_id` INT NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `is_sold_out` TINYINT NOT NULL,
  `created_on` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rental_quote_company_idx` (`company_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_rental_duration1_idx` (`rental_duration_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_vehicle_model1_idx` (`vehicle_model_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_pick_up_date1_idx` (`pick_up_date_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_pick_up_time1_idx` (`pick_up_time_id` ASC) VISIBLE,
  INDEX `fk_rental_quote_rental_route1_idx` (`rental_route_id` ASC) VISIBLE,
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
  CONSTRAINT `fk_rental_quote_vehicle_model1`
    FOREIGN KEY (`vehicle_model_id`)
    REFERENCES `vehicle_model` (`id`)
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
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `office`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `office` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_id` INT NOT NULL,
  `location_id` INT NOT NULL,
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


-- -----------------------------------------------------
-- Table `office`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `office` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_id` INT NOT NULL,
  `location_id` INT NOT NULL,
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

USE `rentals_scraping` ;

-- -----------------------------------------------------
-- Placeholder table for view `company_rental_route`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `company_rental_route` (`company_id` INT, `rental_route_id` INT, `pick_up_location_id` INT, `pick_up_location_name` INT, `pick_up_location_address` INT, `drop_off_location_id` INT, `drop_off_location_name` INT, `drop_off_location_address` INT);

-- -----------------------------------------------------
-- procedure debug_msg
-- -----------------------------------------------------

DELIMITER $$
USE `rentals_scraping`$$
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
-- View `company_rental_route`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `company_rental_route`;
USE `rentals_scraping`;
CREATE  OR REPLACE VIEW `company_rental_route` AS
    SELECT
        pick_up_office.company_id,
        rental_route.id rental_route_id,
        pick_up_office.location_id pick_up_location_id,
        pick_up_location.name pick_up_location_name,
        pick_up_office.address pick_up_location_address,
        drop_off_office.location_id drop_off_location_id,
        drop_off_location.name drop_off_location_name,
        drop_off_office.address drop_off_location_address
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
insert into company(id, name) values(3, 'GO Rentals');
commit;

-- initialze the rental_duration table
insert into rental_duration(id, number_of_days) values(1, 1);
insert into rental_duration(id, number_of_days) values(2, 2);
insert into rental_duration(id, number_of_days) values(3, 3);
insert into rental_duration(id, number_of_days) values(4, 4);
insert into rental_duration(id, number_of_days) values(5, 5);

-- initialze the pick_up_time table
insert into pick_up_time(id, value) values(1, sec_to_time(9*60*60)); -- 09:00 AM
insert into pick_up_time(id, value) values(2, sec_to_time(13*60*60)); -- 01:00 PM
-- end attached script 'script'
