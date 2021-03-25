create table places
(
    place_id bigserial PRIMARY KEY,
    name text not null
);

create table cities
(
    city_id smallserial PRIMARY KEY,
    name text not null
);

create table users
(
    tg_id bigserial PRIMARY KEY,
    music_preferences varchar[] not null
    vk_id bigint 
    spotify_id bigint
);

create table useinter
(
    tg_id bigint not null,
    inter_datetime timestamp not null,
    inter_type_id smallint not null
);

create table interactions
(
    inter_type_id smallserial PRIMARY KEY,
    inter_name varchar not null
);

create table concerts
(
    concert_id bigserial PRIMARY KEY,
    concert_name text not null,
    place_id bigint not null,
    city_id smallint not null,
    datetime timestamp not null,
    price smallint,
    concert_comment text
);

create table musicians
(
    musician_id bigserial PRIMARY KEY,
    musician_name varchar not null
);

create table conmus
(
    concert_id bigint not null,
    musician_id bigint not null
);

create table usemus
(
    tg_id bigint not null,
    musician_id bigint not null
);
