CREATE TABLE news_to_tags (
    id SERIAL PRIMARY KEY,
    news_id INT NOT NULL REFERENCES news (id) ON UPDATE CASCADE ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES tags (id) ON UPDATE CASCADE,
    CONSTRAINT news_tag_pkey UNIQUE (news_id, tag_id)
);
