--Отримати всі завдання певного користувача.
select * from tasks where user_id = 555


--Вибрати завдання за певним статусом
select * 
from tasks 
where status_id = (
	select id from status where name = 'new'	
);

--Оновити статус конкретного завдання
update tasks t
set status_id = (
	select id from status where name = 'in progress'	
)
where t.id = 396
--Для перевірки:
--select * from tasks where id = 396

--Отримати список користувачів, які не мають жодного завдання
select *
from users u
where u.id not in (
	select user_id from tasks
);


--Додати нове завдання для конкретного користувача
insert into tasks ( title, description, status_id, user_id)
values ('new task', 'new task description', (select id from status where name = 'new'), 154);
--Для перевірки:
--select * from tasks where user_id = 154


--Отримати всі завдання, які ще не завершено
select *
from tasks t
where t.status_id in (
	select id from status where name <> 'completed'
);


--Видалити конкретне завдання
delete from tasks 
where id = 20


--Знайти користувачів з певною електронною поштою
select *
from users
where email like '%y@example.net'


--Оновити ім'я користувача
update users 
set fullname = 'Тарас Попандопало'
where id = 555


--Отримати кількість завдань для кожного статусу
select count(tasks.id), status.name
from tasks
left join status
on tasks.status_id = status.id 
group by status.name


--Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
select tasks.id, tasks.title, tasks.description, tasks.status_id, users.fullname, users.email 
from tasks
left join users
on tasks.user_id = users.id
where users.email like '%@example.com'


--Отримати список завдань, що не мають опису
select *
from tasks
where tasks.description = ''
