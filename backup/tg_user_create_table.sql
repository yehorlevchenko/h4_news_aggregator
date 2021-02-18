CREATE TABLE tg_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(1024) NOT NULL,
    first_name VARCHAR(1024),
    second_name VARCHAR(1024),
    language_code VARCHAR(10) NOT NULL
);

CREATE UNIQUE INDEX tg_user_id ON tg_user (id);
