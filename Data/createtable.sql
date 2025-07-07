/* Check that the table doesn't already exist in the database. If it does,remove it from the database */
DROP TABLE IF EXISTS songs;

/* Create the table in the database & give it a name */
CREATE TABLE songs (

/* Tell the database which data to import, what its name in the database should be, & the type of data to import */
    
    artist text,
    track_name text,
    track_id varchar(22),
    popularity smallint,
    year_released smallint,
    genre varchar(15),
    danceability numeric(4,3),
    energy numeric(4,3),
    key smallint,
    loudness numeric(6,3),
    mode numeric(1,0),
    valence numeric(4,3),
    tempo numeric(6,3),
    duration_ms integer,

    PRIMARY KEY (track_id)
);

