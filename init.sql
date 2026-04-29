set names utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


drop table if exists users;
create table users (
    user_id bigint primary key auto_increment,
    login varchar(50) unique not null,
    password varchar(255) not null,
    email varchar(255) unique not null,
    reg_dt datetime not null default current_timestamp
);

drop table if exists priorities;
create table priorities (
    priority_id bigint primary key auto_increment,
    priority_title varchar(25) unique not null
);

drop table if exists statuses;
create table statuses (
    status_id bigint primary key auto_increment,
    status_title varchar(25) unique not null
);

drop table if exists tasks;
create table tasks (
    task_id bigint primary key auto_increment,
    task_title varchar(255) unique not null,
    description text,
    deadline datetime,
    author_id bigint not null,

    foreign key (author_id) references users(user_id) on delete cascade on update cascade
);

drop table if exists task_assignee;
create table task_assignee (
    task_assignee_id bigint primary key auto_increment,
    task_id bigint not null,
    assignee_id bigint,
    assignee_dt datetime not null default current_timestamp,

    foreign key (task_id) references tasks(task_id) on delete cascade on update cascade,
    foreign key (assignee_id) references users(user_id) on delete set null on update set null
);

drop table if exists task_priority;
create table task_priority (
    task_priority_id bigint primary key auto_increment,
    task_id bigint not null,
    priority_id bigint,
    priority_dt datetime not null default current_timestamp,

    foreign key (task_id) references tasks(task_id) on delete cascade on update cascade,
    foreign key (priority_id) references priorities(priority_id) on delete cascade on update restrict
);

drop table if exists task_status;
create table task_status (
    task_status_id bigint primary key auto_increment,
    task_id bigint not null,
    status_id bigint not null,
    status_dt datetime not null default current_timestamp,

    foreign key (task_id) references tasks(task_id) on delete cascade on update cascade,
    foreign key (status_id) references statuses(status_id) on delete cascade on update restrict
);

-- ============================================
-- Мок-данные для сервиса задач
-- Совместимо с MySQL 8.0, кодировка utf8mb4
-- ============================================

-- ================== ПОЛЬЗОВАТЕЛИ ==================
INSERT INTO users (login, password, email, reg_dt) VALUES
('alice',   '$argon2id$v=19$m=65536,t=3,p=4$...$...', 'alice@example.com', '2026-04-01 10:00:00'),
('bob',     '$argon2id$v=19$m=65536,t=3,p=4$...$...', 'bob@example.com',   '2026-04-02 11:00:00'),
('charlie', '$argon2id$v=19$m=65536,t=3,p=4$...$...', 'charlie@example.com','2026-04-03 12:00:00'),
('diana',   '$argon2id$v=19$m=65536,t=3,p=4$...$...', 'diana@example.com', '2026-04-04 09:30:00'),
('eve',     '$argon2id$v=19$m=65536,t=3,p=4$...$...', 'eve@example.com',   '2026-04-05 11:00:00'),
('frank',   '$argon2id$v=19$m=65536,t=3,p=4$...$...', 'frank@example.com', '2026-04-06 14:00:00');

-- ================== СТАТУСЫ ==================
INSERT INTO statuses (status_title) VALUES
('Создана'),
('В работе'),
('Выполнена'),
('Закрыта');

-- ================== ПРИОРИТЕТЫ ==================
INSERT INTO priorities (priority_title) VALUES
('Низкий'),
('Средний'),
('Высокий'),
('Критичный');

-- ================== ЗАДАЧИ ==================
INSERT INTO tasks (task_title, description, deadline, author_id) VALUES
('Разработать API аутентификации', 'Реализовать JWT-токены и эндпоинты login/signup', NULL, 1),
('Сверстать главную страницу', 'Адаптивная вёрстка с использованием React и CSS Grid', NULL, 2),
('Настроить CI/CD', 'Написать пайплайн для автодеплоя на сервер', NULL, 1),
('Рефакторинг модуля задач', 'Улучшить структуру кода и добавить тесты', NULL, 3),
('Подготовить документацию', 'Описать API в Swagger', NULL, 2),
('Обновить дизайн логотипа', 'Разработать новый логотип для продукта', NULL, 1),
('Написать unit-тесты', NULL, NULL, 2),
('Развернуть staging-сервер', 'Настроить сервер для тестирования', '2026-05-01 00:00:00', 3),
('Провести код-ревью', NULL, NULL, 4),
('Обновить зависимости', 'Обновить библиотеки до последних версий', NULL, 1),
('Миграция базы данных', 'Выполнить миграцию на новую версию схемы', '2026-04-30 10:00:00', 2);

-- ================== ИСПОЛНИТЕЛИ ==================
INSERT INTO task_assignee (task_id, assignee_id, assignee_dt) VALUES
-- Задача 1
(1, 2, '2026-04-05 10:00:00'),
(1, 3, '2026-04-07 14:00:00'),
-- Задача 2
(2, 1, '2026-04-06 09:00:00'),
-- Задача 3
(3, 3, '2026-04-08 11:00:00'),
(3, 2, '2026-04-10 16:00:00'),
-- Задача 4
(4, 4, '2026-04-09 12:00:00'),
-- Задача 5
(5, 1, '2026-04-11 08:00:00'),
-- Задача 6
(6, 5, '2026-04-12 10:00:00'),
-- Задача 7
(7, 6, '2026-04-12 11:00:00'),
-- Задача 8
(8, 4, '2026-04-13 09:00:00'),
(8, 6, '2026-04-14 14:00:00'),
-- Задача 9
(9, 1, '2026-04-13 10:00:00'),
-- Задача 10
(10, 2, '2026-04-14 09:00:00'),
-- Задача 11
(11, 3, '2026-04-14 11:00:00');

-- ================== ИСТОРИЯ ПРИОРИТЕТОВ ==================
INSERT INTO task_priority (task_id, priority_id, priority_dt) VALUES
-- Задача 1
(1, 3, '2026-04-05 10:00:00'),
(1, 2, '2026-04-07 14:00:00'),
-- Задача 2
(2, 2, '2026-04-06 09:00:00'),
-- Задача 3
(3, 4, '2026-04-08 11:00:00'),
(3, 3, '2026-04-10 16:00:00'),
-- Задача 4
(4, 1, '2026-04-09 12:00:00'),
-- Задача 5
(5, 3, '2026-04-11 08:00:00'),
-- Задача 6
(6, 1, '2026-04-12 10:00:00'),
-- Задача 7
(7, 2, '2026-04-12 11:00:00'),
-- Задача 8
(8, 3, '2026-04-13 09:00:00'),
-- Задача 9
(9, 4, '2026-04-13 10:00:00'),
(9, 2, '2026-04-14 12:00:00'),
-- Задача 10
(10, 1, '2026-04-14 09:00:00'),
-- Задача 11
(11, 3, '2026-04-14 11:00:00');

-- ================== ИСТОРИЯ СТАТУСОВ ==================
INSERT INTO task_status (task_id, status_id, status_dt) VALUES
-- Задача 1
(1, 1, '2026-04-05 10:00:00'),
(1, 2, '2026-04-06 15:00:00'),
(1, 1, '2026-04-08 09:00:00'),
(1, 2, '2026-04-10 11:00:00'),
(1, 3, '2026-04-14 16:00:00'),
(1, 4, '2026-04-15 10:00:00'),
-- Задача 2
(2, 1, '2026-04-06 09:00:00'),
(2, 2, '2026-04-07 11:00:00'),
(2, 3, '2026-04-10 17:00:00'),
(2, 4, '2026-04-11 08:00:00'),
-- Задача 3
(3, 1, '2026-04-08 11:00:00'),
(3, 2, '2026-04-09 10:00:00'),
(3, 3, '2026-04-12 14:00:00'),
(3, 1, '2026-04-13 09:00:00'),
(3, 2, '2026-04-14 12:00:00'),
(3, 3, '2026-04-17 16:00:00'),
(3, 4, '2026-04-18 10:00:00'),
-- Задача 4
(4, 1, '2026-04-09 12:00:00'),
(4, 2, '2026-04-10 14:00:00'),
(4, 3, '2026-04-11 17:00:00'),
-- Задача 5
(5, 1, '2026-04-11 08:00:00'),
(5, 2, '2026-04-12 09:00:00'),
(5, 2, '2026-04-13 08:00:00'),
(5, 3, '2026-04-18 14:00:00'),
(5, 4, '2026-04-19 10:00:00'),
-- Задача 6
(6, 1, '2026-04-12 10:00:00'),
(6, 2, '2026-04-13 14:00:00'),
(6, 3, '2026-04-16 09:00:00'),
(6, 4, '2026-04-17 12:00:00'),
-- Задача 7
(7, 1, '2026-04-12 11:00:00'),
(7, 2, '2026-04-13 10:00:00'),
(7, 1, '2026-04-14 08:00:00'),
(7, 2, '2026-04-15 14:00:00'),
(7, 3, '2026-04-17 16:00:00'),
-- Задача 8
(8, 1, '2026-04-13 09:00:00'),
(8, 2, '2026-04-14 10:00:00'),
(8, 3, '2026-04-16 15:00:00'),
-- Задача 9
(9, 1, '2026-04-13 10:00:00'),
(9, 2, '2026-04-14 12:00:00'),
(9, 3, '2026-04-18 09:00:00'),
(9, 4, '2026-04-19 11:00:00'),
-- Задача 10
(10, 1, '2026-04-14 09:00:00'),
(10, 2, '2026-04-16 11:00:00'),
-- Задача 11
(11, 1, '2026-04-14 11:00:00'),
(11, 2, '2026-04-15 14:00:00'),
(11, 3, '2026-04-18 16:00:00'),
(11, 4, '2026-04-20 10:00:00');