CREATE DATABASE IF NOT EXISTS movie_metadata;
USE movie_metadata;

-- Table for movie basics
DROP TABLE IF EXISTS title_basics;
CREATE TABLE title_basics (
    tconst VARCHAR(20) PRIMARY KEY,
    titleType VARCHAR(50),
    primaryTitle VARCHAR(255),
    originalTitle VARCHAR(255),
    isAdult BOOLEAN,
    startYear INT,
    endYear INT DEFAULT NULL,
    runtimeMinutes INT DEFAULT NULL,
    genres VARCHAR(255)
);

-- Table for ratings
DROP TABLE IF EXISTS title_ratings;
CREATE TABLE title_ratings (
    tconst VARCHAR(20),
    averageRating FLOAT,
    numVotes INT,
    PRIMARY KEY (tconst),
    FOREIGN KEY (tconst) REFERENCES title_basics(tconst)
);

-- Table for cast and crew
DROP TABLE IF EXISTS title_principals;
CREATE TABLE title_principals (
    tconst VARCHAR(20),
    ordering INT,
    nconst VARCHAR(20),
    category VARCHAR(100),
    job VARCHAR(255),
    characters TEXT,
    PRIMARY KEY (tconst, ordering),
    FOREIGN KEY (tconst) REFERENCES title_basics(tconst)
);