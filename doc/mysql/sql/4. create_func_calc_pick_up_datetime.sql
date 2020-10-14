delimiter $$
drop function if exists calc_pick_up_datetime$$
create function calc_pick_up_datetime(
	base_pick_up_datetime datetime, 
	type varchar(16), 
	index_in_array int, 
	time_gap int
) returns datetime
deterministic
begin
	declare error_message varchar(256) default '';
	if type = 'extend' then
		return base_pick_up_datetime;
	elseif type = 'delay' then
		return date_add(base_pick_up_datetime, interval (index_in_array * time_gap * 30) MINUTE);
    else
		set error_message = concat('Unknown type: ', type);
		signal sqlstate '45000' set MESSAGE_TEXT = error_message;
	end if;
end$$
delimiter ;