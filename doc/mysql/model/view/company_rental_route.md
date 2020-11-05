```sql
CREATE VIEW `company_rental_route` AS
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
            AND rental_route.drop_off_location_id = drop_off_location.id
```
