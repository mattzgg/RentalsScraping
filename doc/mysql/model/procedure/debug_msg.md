```sql
CREATE PROCEDURE `debug_msg`(
in enabled int,
in msg varchar(255)
)
BEGIN
	if enabled then
		select concat('** ', msg) as '** DEBUG:';
	end if;
END
```
