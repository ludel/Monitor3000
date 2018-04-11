create table site
(
  id  INTEGER
    primary key
                   autoincrement,
  url VARCHAR(200) default empty
);

create table requests
(
  id     INTEGER
    primary key
                  autoincrement,
  number INTEGER  default 0,
  siteId INTEGER not null
    constraint requests_site_id_fk
    references site
      on delete cascade,
  date   DATETIME default current_timestamp
);

create table user
(
  id       INTEGER
    primary key
  autoincrement,
  pseudo   VARCHAR(100) not null,
  password VARCHAR(100) not null
);
