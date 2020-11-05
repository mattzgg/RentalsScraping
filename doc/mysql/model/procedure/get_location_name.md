```sql
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
END
```
