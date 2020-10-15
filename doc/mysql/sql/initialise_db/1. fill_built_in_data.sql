insert into company(id, name) values(1, 'Thrifty');
insert into company(id, name) values(2, 'Budget');
insert into company(id, name) values(3, 'GO Rentals');
commit;

insert into rental_duration_operation(id, type, time_gap, array_size, description) values(1, 'delay', 48, 30, 'Used to observe everyday price in a month');
insert into rental_duration_operation(id, type, time_gap, array_size, description) values(2, 'extend', 1, 25, 'Used to observe price change when rental duration is extended from 1 day to 2 days');
commit;