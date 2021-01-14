CREATE TABLE news (
    id SERIAL,
    source_api VARCHAR(50) NOT NULL,
    title VARCHAR(512) NOT NULL,
    abstract TEXT,
    slug_name VARCHAR(128),
    published_date TIMESTAMP NOT NULL,
    url TEXT NOT NULL,
    internal_source VARCHAR(256),
    media_url TEXT
);
