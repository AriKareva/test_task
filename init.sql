set names utf8mb4;
drop table if exists users;
create table users (
    user_id bigint primary key auto_increment,
    login varchar(50) unique not null,
    password varchar(255) not null,
    email varchar(255) unique not null,
    reg_dt datetime not null default current_timestamp
);

drop table if exists tasks;
create table tasks (
    task_id bigint primary key auto_increment,
    task_title varchar(255) unique not null,
    description text,
    priority int,
    author_id bigint not null,
    assignee_id bigint not null
);

drop table if exists task_status;
create table task_status (
    task_status_id bigint primary key auto_increment,
    task_id bigint not null,
    status_id bigint not null,
    start_dt datetime default current_timestamp,
    end_dt datetime default current_timestamp
);

drop table if exists statuses;
create table statuses (
    status_id bigint primary key auto_increment,
    status_title varchar(25) unique not null
);

drop table if exists task_file;
create table task_file (
    task_file_id bigint primary key auto_increment,
    task_id bigint not null,
    file_id bigint
);

drop table if exists files;
create table files (
    file_id bigint primary key auto_increment,
    file_name varchar(255) not null,
    upload_dt datetime not null default current_timestamp
);

insert into users (login, password, email, reg_dt) values
('alice',   '$2b$12$LJ3m4ys3GZ5zWuK5g6P6YOqk7Hq7WqCj1GZ5zWuK5g6P6YOqk7Hq7W', 'alice@example.com', '2026-04-01 10:00:00'),
('bob',     '$2b$12$LJ3m4ys3GZ5zWuK5g6P6YOqk7Hq7WqCj1GZ5zWuK5g6P6YOqk7Hq7W', 'bob@example.com',   '2026-04-02 11:00:00'),
('charlie', '$2b$12$LJ3m4ys3GZ5zWuK5g6P6YOqk7Hq7WqCj1GZ5zWuK5g6P6YOqk7Hq7W', 'charlie@example.com', '2026-04-03 12:00:00');


insert into tasks (task_title, description, priority, author_id, assignee_id) values
('Создать макет главной страницы', 'Разработать дизайн и сверстать главную страницу', 2, 1, 2),
('Написать документацию api',      'Документировать все эндпоинты в swagger', 1, 1, 3),
('Настроить ci/cd',               'Написать пайплайн для автоматического деплоя', 3, 2, 1),
('Пофиксить баг с авторизацией',   'При повторном логине не обновляется токен', 1, 3, 1),
('Рефакторинг модуля задач',       'Улучшить структуру кода в соответствии с паттернами', 2, 2, 3);


insert into statuses (status_title) values
('to do'),
('in progress'),
('done'),
('on review');


insert into task_status (task_id, status_id, start_dt) values
(1, 2, '2026-04-10 09:00:00'),
(2, 1, '2026-04-11 10:00:00'),
(3, 3, '2026-04-09 15:00:00'),
(4, 1, '2026-04-12 08:00:00'),
(5, 2, '2026-04-13 14:00:00');


insert into files (file_name, upload_dt) values
('design_mockup.png', '2026-04-10 12:00:00'),
('api_doc.pdf',       '2026-04-11 13:00:00'),
('cicd_pipeline.yml', '2026-04-09 16:00:00');


insert into task_file (task_id, file_id) values
(1, 1),
(2, 2),
(3, 3);