Create database peep_app_schema;
Use peep_app_schema;

Create table roles (
	id int primary key auto_increment,
    name varchar(45)
);

Create table user_status (
	id int primary key auto_increment,
    name varchar(45)
);

Create table countries (
	id int primary key auto_increment,
    name varchar(45),
    iso varchar(3)
);

Create table users (
	id int primary key auto_increment,
    firstname varchar(45),
    lastname varchar(45),
    birthday date,
    gender varchar(100),
    username varchar(50),
    email varchar(100) unique,
    password text,
    created_at datetime,
    updated_at datetime,
    token text,
    status_id int not null,
    role_id int not null,
	country_id int not null,
    foreign key (status_id) references user_status(id),
    foreign key (role_id) references roles(id),
    foreign key (country_id) references countries(id)
);

Create table followers (
	follower int not null,
    followed int not null,
    foreign key (follower) references users(id) on delete cascade,
	foreign key (followed) references users(id) on delete cascade
);

Create table collections (
	id int primary key auto_increment,
    name varchar(100),
    description text,
    owner_id int not null,
	created_at datetime,
    updated_at datetime,
    foreign key (owner_id) references users(id) on delete cascade
);

Create table posts (
	id int primary key auto_increment,
    content text,
    author_id int not null,
	created_at datetime,
    updated_at datetime,
    foreign key (author_id) references users(id) on delete cascade
);

Create table collections_has_posts (
	collection_id int not null,
    post_id int not null,
    foreign key (collection_id) references collections(id) on delete cascade,
    foreign key (post_id) references posts(id) on delete cascade
);

Create table posts_images (
	id int primary key auto_increment,
    url text,
    post_id int not null,
	created_at datetime,
    updated_at datetime,
    foreign key (post_id) references posts(id) on delete cascade
);

Create table posts_has_likes (
    post_id int not null,
    user_id int not null,
    foreign key (post_id) references posts(id) on delete cascade,
    foreign key (user_id) references users(id) on delete cascade
);

Create table comments (
	id int primary key auto_increment,
    content text,
	created_at datetime,
    updated_at datetime,
    author_id int not null,
    post_id int not null,
    foreign key (author_id) references users(id) on delete cascade,
    foreign key (post_id) references posts(id) on delete cascade
);

Create table comments_has_likes (
	comment_id int not null,
	user_id int not null,
    foreign key (comment_id) references comments(id) on delete cascade,
    foreign key (user_id) references users(id) on delete cascade
);

Create table reports (
    id int primary key auto_increment,
    user_id int not null,
    user_ip varchar(45),
	isDeleted boolean default false,
    created_at datetime,
    updated_at datetime,
    foreign key (user_id) references users (id)
);

# --- #

Insert into roles(name) values ('Administrator'), ('User');
Insert into user_status(name) values('Pending'), ('Active'), ('Blocked'), ('Deleted');
Insert into countries(name, iso) values ('Argentina', 'ARG'), ('Bolivia', 'BOL'), ('Brazil', 'BRA'), ('Chile', 'CHL'), ('Colombia', 'COL'), ('Ecuador', 'ECU'), ('Mexico', 'MEX'), ('Peru', 'PER'), ('Uruguay', 'URY'), ('Venezuela', 'VEN');
