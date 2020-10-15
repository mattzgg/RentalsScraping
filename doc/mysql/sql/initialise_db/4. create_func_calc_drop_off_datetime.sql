delimiter $$
drop function if exists calc_drop_off_datetime$$
create function calc_drop_off_datetime(
	base_drop_off_datetime datetime, 
	type varchar(16), 
	index_in_array int, 
	time_gap int
) returns datetime
deterministic
begin
	declare error_message varchar(256) default '';
	if type = 'extend' or type = 'delay' then
		return date_add(base_drop_off_datetime, interval (index_in_array * time_gap * 30) minute);
    else
		set error_message = concat('Unknown type: ', type);
		signal sqlstate '45000' set MESSAGE_TEXT = error_message;
	end if;
end$$
delimiter ;