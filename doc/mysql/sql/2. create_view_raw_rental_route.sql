CREATE VIEW `raw_rental_route` AS
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
    pul.company_id = dol.company_id