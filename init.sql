set names utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Очистка таблиц в правильном порядке (из-за внешних ключей)
DELETE FROM statuses;
DELETE FROM priorities;
DELETE FROM users;
DELETE FROM task_file;
DELETE FROM task_status;
DELETE FROM task_priority;
DELETE FROM task_assignee;
DELETE FROM tasks;


-- Сброс автоинкремента
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE priorities AUTO_INCREMENT = 1;
ALTER TABLE statuses AUTO_INCREMENT = 1;
ALTER TABLE tasks AUTO_INCREMENT = 1;
ALTER TABLE task_assignee AUTO_INCREMENT = 1;
ALTER TABLE task_priority AUTO_INCREMENT = 1;
ALTER TABLE task_status AUTO_INCREMENT = 1;
ALTER TABLE task_file AUTO_INCREMENT = 1;


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
('diana',   '$argon2id$v=19$m=65536,t=3,p=4$...$...', 'diana@example.com', '2026-04-04 09:30:00');

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
('Разработать API аутентификации', 'Реализовать JWT-токены и эндпоинты login/signup', null, 1),
('Сверстать главную страницу', 'Адаптивная вёрстка с использованием React и CSS Grid',null, 2),
('Настроить CI/CD', 'Написать пайплайн для автодеплоя на сервер', null, 1),
('Рефакторинг модуля задач', 'Улучшить структуру кода и добавить тесты', null, 3),
('Подготовить документацию', 'Описать API в Swagger', null, 2);

-- ================== ИСПОЛНИТЕЛИ (текущие/исторические) ==================
-- Для каждой задачи добавляем текущего исполнителя и предысторию
INSERT INTO task_assignee (task_id, assignee_id, assignee_dt) VALUES
-- Задача 1: сначала взял Bob, потом передал Charlie
(1, 2, '2026-04-05 10:00:00'),
(1, 3, '2026-04-07 14:00:00'),
-- Задача 2: выполняет Alice
(2, 1, '2026-04-06 09:00:00'),
-- Задача 3: взял Charlie, потом вернул Bob'у
(3, 3, '2026-04-08 11:00:00'),
(3, 2, '2026-04-10 16:00:00'),
-- Задача 4: выполняет Diana
(4, 4, '2026-04-09 12:00:00'),
-- Задача 5: выполняет Alice
(5, 1, '2026-04-11 08:00:00');

-- ================== ИСТОРИЯ ПРИОРИТЕТОВ ==================
INSERT INTO task_priority (task_id, priority_id, priority_dt) VALUES
(1, 3, '2026-04-05 10:00:00'), -- Высокий
(1, 2, '2026-04-07 14:00:00'), -- Средний
(2, 2, '2026-04-06 09:00:00'), -- Средний
(3, 4, '2026-04-08 11:00:00'), -- Критичный
(3, 3, '2026-04-10 16:00:00'), -- Высокий
(4, 1, '2026-04-09 12:00:00'), -- Низкий
(5, 3, '2026-04-11 08:00:00'); -- Высокий

-- ================== ИСТОРИЯ СТАТУСОВ ==================
INSERT INTO task_status (task_id, status_id, status_dt) VALUES
(1, 1, '2026-04-05 10:00:00'), -- Создана
(1, 2, '2026-04-06 15:00:00'), -- В работе
(2, 1, '2026-04-06 09:00:00'), -- Создана
(2, 2, '2026-04-07 11:00:00'), -- В работе
(2, 3, '2026-04-10 17:00:00'), -- Выполнена
(3, 1, '2026-04-08 11:00:00'), -- Создана
(3, 2, '2026-04-09 10:00:00'), -- В работе
(4, 1, '2026-04-09 12:00:00'), -- Создана
(5, 1, '2026-04-11 08:00:00'); -- Создана


SET FOREIGN_KEY_CHECKS = 1;