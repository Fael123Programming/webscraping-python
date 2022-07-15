CREATE DATABASE ifgoiano_publications;

\c ifgoiano_publications;

CREATE TABLE post_category (
    pk_post_category SERIAL PRIMARY KEY,
    category_description VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE website_post (
    pk_post SERIAL PRIMARY KEY,
    fk_post_category INTEGER NOT NULL,
    post_title VARCHAR(100) NOT NULL,
    post_description VARCHAR(200) NOT NULL,
    post_publication_timestamp TIMESTAMP NOT NULL,
    post_accesses INTEGER NOT NULL CHECK (post_accesses >= 0),
    relevance_index NUMERIC(5, 2) NOT NULL CHECK(relevance_index >= 0),
    FOREIGN KEY (fk_post_category) REFERENCES post_category (pk_post_category) ON UPDATE CASCADE ON DELETE RESTRICT
);
