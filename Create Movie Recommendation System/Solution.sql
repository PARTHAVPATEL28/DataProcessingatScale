CREATE TABLE users (
    userid int NOT NULL PRIMARY KEY,
    name text NOT NULL  
);

CREATE TABLE movies (
    movieid integer NOT NULL PRIMARY KEY,
    title text NOT NULL 
);

CREATE TABLE taginfo (
    tagid int NOT NULL PRIMARY KEY,
    content text NOT NULL 
);

CREATE TABLE genres (
    genreid integer NOT NULL PRIMARY KEY,
    name text NOT NULL 
);


CREATE TABLE ratings(
userid int  REFERENCES users(userid) ON DELETE CASCADE,  
movieid int  REFERENCES movies(movieid) ON DELETE CASCADE,  
rating  numeric NOT NULL check(rating>=0 and rating<=5),
timestamp bigint NOT NULL,
CONSTRAINT PK_ratings PRIMARY KEY (userid, movieid)
);



CREATE TABLE tags(
userid int  REFERENCES users(userid) ON DELETE CASCADE,
movieid int  REFERENCES movies(movieid) ON DELETE CASCADE,
tagid int  REFERENCES taginfo(tagid) ON DELETE CASCADE,
timestamp bigint NOT NULL,
CONSTRAINT PK_tags PRIMARY KEY (userid, movieid,tagid)
);

CREATE TABLE hasagenre(
movieid int  REFERENCES movies(movieid) ON DELETE CASCADE,
genreid int   REFERENCES genres(genreid) ON DELETE CASCADE,
CONSTRAINT PK_hasagenre PRIMARY KEY (movieid, genreid)
);
