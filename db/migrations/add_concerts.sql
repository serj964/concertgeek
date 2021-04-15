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