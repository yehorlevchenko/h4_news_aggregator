CREATE TABLE tags (
    id SERIAL,
    source_api VARCHAR(50) NOT NULL,
    tag_name VARCHAR(256) NOT NULL,
    tag_group VARCHAR(256)
);

CREATE UNIQUE INDEX original_tags ON tags (source_api, tag_name, tag_group);

ALTER TABLE tags ADD CONSTRAINT original_tags UNIQUE USING INDEX original_tags;