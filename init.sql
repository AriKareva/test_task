set names utf8mb4;
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

drop table if exists task_file;
create table task_file (
    task_file_id bigint primary key auto_increment,
    task_id bigint not null,
    file_name varchar(255) not null,
    upload_dt datetime not null default current_timestamp,

    foreign key (task_id) references tasks(task_id) on delete cascade on update cascade
);
