CREATE TABLE tags (
    id SERIAL,
    source_api VARCHAR(50) NOT NULL,
    name VARCHAR(256) NOT NULL,
    group VARCHAR(256)
);
