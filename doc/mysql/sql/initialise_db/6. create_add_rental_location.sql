delimiter $$
drop procedure if exists add_rental_location$$
create procedure add_rental_location(
	in name varchar(255), 
	in input_value varchar(255),
    in company_id int,
    out record_id int
) 
deterministic
begin
    select t.id into record_id from location t where t.name = name and t.company_id = company_id;
    if record_id is null then
		insert into location(name, input_value, company_id) values(name, input_value, company_id);
        select last_insert_id() into record_id;
	else
		update location t set t.input_value = input_value where t.name = name and t.company_id = company_id;
	end if;
end$$
delimiter ;