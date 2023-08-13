import psycopg2

# create database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="admin",
    host="127.0.0.1"
)

cursor = conn.cursor()
conn.autocommit = True

drop_movies_db_sql = "DROP DATABASE IF EXISTS movies"

create_movies_db_sql = "CREATE DATABASE movies"

cursor.execute(drop_movies_db_sql)
cursor.execute(create_movies_db_sql)

cursor.close()
conn.close()

# create tables
conn = psycopg2.connect(
    dbname="movies",
    user="postgres",
    password="admin",
    host="127.0.0.1"
)

cursor = conn.cursor()
conn.autocommit = True

create_persons_table_sql = """CREATE TABLE person (
    person_id SERIAL PRIMARY KEY,
    person_firstname VARCHAR(50) NOT NULL,
    person_lastname VARCHAR(50) NOT NULL,
    person_birthdate DATE NOT NULL,
    person_deathdate DATE,
    person_place_born VARCHAR(100) NOT NULL,
    person_nationality VARCHAR(100) NOT NULL,
    person_description TEXT
)"""

create_actors_table_sql = """CREATE TABLE actor (
    actor_id INT PRIMARY KEY,
    actor_alma_mater TEXT,
    FOREIGN KEY (actor_id) REFERENCES person(person_id)
)"""

create_directors_table_sql = """CREATE TABLE director (
    director_id INT PRIMARY KEY,
    FOREIGN KEY (director_id) REFERENCES person(person_id)
)"""

create_movies_table_sql = """CREATE TABLE movie (
    movie_id SERIAL PRIMARY KEY,
    movie_title VARCHAR(150) NOT NULL,
    movie_about TEXT NOT NULL,
    movie_release_date DATE NOT NULL,
    director_id INT NOT NULL,
    movie_distributor VARCHAR(50) NOT NULL,
    movie_budget_usd NUMERIC(18,2) NOT NULL,
    movie_boxoffice_usd NUMERIC(18,2) NOT NULL,
    movie_imdb NUMERIC(3, 1) NOT NULL,
    movie_google_liked INT NOT NULL,
    FOREIGN KEY (director_id) REFERENCES director(director_id)
)"""

create_movie_actors_table_sql = """CREATE TABLE actor_movie (
    actor_id INT NOT NULL,
    movie_id INT NOT NULL,
    actor_movie_role VARCHAR(100) NOT NULL,
    actor_movie_notes TEXT NOT NULL,
    PRIMARY KEY (actor_id, movie_id),
    FOREIGN KEY (actor_id) REFERENCES actor(actor_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
)"""

cursor.execute(create_persons_table_sql)
cursor.execute(create_actors_table_sql)
cursor.execute(create_directors_table_sql)
cursor.execute(create_movies_table_sql)
cursor.execute(create_movie_actors_table_sql)

# add columns
add_column_actors_table_sql = """ALTER TABLE actor 
ADD COLUMN actor_height_meters NUMERIC(3, 2) NOT NULL"""

add_column_movies_table_sql = """ALTER TABLE movie 
ADD COLUMN movie_release_country VARCHAR(50) NOT NULL"""

cursor.execute(add_column_actors_table_sql)
cursor.execute(add_column_movies_table_sql)

# drop columns
drop_column_movies_table_sql = """ALTER TABLE movie 
DROP COLUMN movie_google_liked"""

drop_column_actors_table_sql = """ALTER TABLE actor 
DROP COLUMN actor_alma_mater"""

cursor.execute(drop_column_movies_table_sql)
cursor.execute(drop_column_actors_table_sql)

# drop and re-create actor_movie table
drop_actor_movie_table_sql = "DROP TABLE actor_movie"

create_new_actor_movie_table_sql = """CREATE TABLE actor_movie (
    actor_id INT NOT NULL,
    movie_id INT NOT NULL,
    actor_movie_roles VARCHAR(100) [] NOT NULL,
    actor_movie_notes TEXT,
    PRIMARY KEY (actor_id, movie_id),
    FOREIGN KEY (actor_id) REFERENCES actor(actor_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id)
)"""

cursor.execute(drop_actor_movie_table_sql)
cursor.execute(create_new_actor_movie_table_sql)

cursor.close()
conn.close()
