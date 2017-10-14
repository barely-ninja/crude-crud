DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS cities;
CREATE TABLE regions (
    region_id INTEGER PRIMARY KEY,
    code text NOT NULL UNIQUE,
    name text NOT NULL UNIQUE
);
CREATE TABLE cities (
    city_id INTEGER PRIMARY KEY,
    name text NOT NULL,
    region_code text NOT NULL,
    FOREIGN KEY (region_code) REFERENCES regions (code)
);
CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY,
    name text NOT NULL,
    last_name text NOT NULL,
    middle_name text,
    phone text UNIQUE,
    email text UNIQUE,
    city_id INTEGER NOT NULL,
    region_code text NOT NULL,
    comment text NOT NULL,
    FOREIGN KEY (region_code) REFERENCES regions (code),
    FOREIGN KEY (city_id) REFERENCES cities (city_id)
);
INSERT INTO regions (code, name) VALUES ( "23", "Краснодарский край" ),( "61", "Ростовская область" ),
( "26", "Ставропольский край");
INSERT INTO cities (name, region_code) VALUES ( "Краснодар", "23" ), ("Кропоткин", "23" ), ("Славянск", "23" );
INSERT INTO cities (name, region_code) VALUES ( "Ростов", "61" ), ("Шахты", "61" ), ("Батайск", "61" );
INSERT INTO cities (name, region_code) VALUES ( "Ставрополь", "26" ), ( "Пятигорск" , "26" ), ( "Кисловодск" , "26" );
 