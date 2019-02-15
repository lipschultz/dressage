DROP TABLE IF EXISTS ratings;

CREATE TABLE ratings (
    file_reference TEXT NOT NULL PRIMARY KEY,
    rating SMALLINT
);