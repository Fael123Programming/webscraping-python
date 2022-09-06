--CREATE DATABASE ifgoiano_publications;
--
--\c ifgoiano_publications;
--
--CREATE TABLE post_category (
--    pk_post_category SERIAL PRIMARY KEY,
--    category_description VARCHAR(50) NOT NULL UNIQUE
--);

--CREATE TABLE weekday (
--    pk_weekday SERIAL PRIMARY KEY,
--    weekday_name TEXT NOT NULL
--);

CREATE TABLE site_post (
    pk_post SERIAL PRIMARY KEY,
    fk_post_category INTEGER NOT NULL,
    fk_weekday INTEGER NOT NULL,
    fk_day_period INTEGER NOT NULL,
    post_title TEXT NOT NULL,
    post_description TEXT,
    post_publication_timestamp TIMESTAMP,
    post_images_count INTEGER NOT NULL CHECK (post_images_count >= 0),
    post_accesses INTEGER CHECK (post_accesses >= 0),
    relevance_index NUMERIC(5, 2) CHECK(relevance_index >= 0),
    FOREIGN KEY (fk_post_category) REFERENCES post_category (pk_post_category) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (fk_weekday) REFERENCES weekday (pk_weekday) ON UPDATE CASCADE ON DELETE NO ACTION,
    FOREIGN KEY (fk_day_period) REFERENCES day_period (pk_day_period) ON UPDATE CASCADE ON DELETE RESTRICT
);

--INSERT INTO weekday (weekday_name) VALUES ('Sun'), ('Mon'), ('Tue'), ('Wed'), ('Thu'), ('Fri'), ('Sat');
--CREATE TABLE day_period (
--    pk_day_period SERIAL PRIMARY KEY,
--    day_period_name TEXT NOT NULL
--);
--INSERT INTO day_period (day_period_name) VALUES ('morning'), ('afternoon'), ('night');
--fk_weekday
--fk_day_period