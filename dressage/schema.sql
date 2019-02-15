DROP TABLE IF EXISTS votes;

CREATE TABLE ratings (
    file_reference TEXT NOT NULL PRIMARY KEY,
    rating SMALLINT
);