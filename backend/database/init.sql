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