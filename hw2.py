import psycopg2

conn = psycopg2.connect(
    dbname="movies",
    user="postgres",
    password="admin",
    host="127.0.0.1"
)

cursor = conn.cursor()
conn.autocommit = True

# create recors
insert_person_table = """INSERT INTO person (person_firstname, person_lastname, person_birthdate, person_place_born, person_nationality, person_description) VALUES 
    ('John', 'Doe', '1990-05-15', 'New York City', 'American', 'Actor known for his versatile roles.'),
    ('Jane', 'Smith', '1985-10-20', 'Los Angeles', 'American', 'Award-winning actress with a diverse portfolio.'),
    ('Michael', 'Johnson', '1978-03-08', 'Chicago', 'American', 'Renowned actor in both theater and film.'),
    ('Emily', 'Brown', '1992-09-03', 'London', 'British', 'Rising star with a captivating screen presence.'),
    ('Alex', 'Garcia', '1982-12-12', 'Barcelona', 'Spanish', 'International actor with a charismatic persona.');"""

insert_actor_table = """INSERT INTO actor (actor_id, actor_height_meters) VALUES 
    (1, 1.75),
    (2, 1.68),
    (3, 1.82),
    (4, 1.63),
    (5, 1.78);"""

insert_director_table = """INSERT INTO director (director_id) VALUES (1),
    (2),
    (3),
    (4),
    (5);"""

insert_movie_table = """INSERT INTO movie (movie_title, movie_about, movie_release_date, director_id, movie_distributor, movie_budget_usd, movie_boxoffice_usd, movie_imdb, movie_release_country) VALUES
    ('The Amazing Adventure', 'A thrilling action-packed adventure.', '2023-08-15', 1, 'Studio Films', 50000000.00, 150000000.00, 8.5, 'United States'),
    ('Mystery of the Shadows', 'A suspenseful mystery unfolding in a small town.', '2023-07-22', 2, 'CineMagic', 30000000.00, 95000000.00, 7.8, 'United Kingdom'),
    ('City of Dreams', 'A drama following the lives of four individuals in a bustling city.', '2023-06-30', 4, 'Urban Films', 40000000.00, 120000000.00, 6.9, 'France'),
    ('Wild Expeditions', 'An epic journey of exploration through untamed lands.', '2023-09-10', 5, 'Adventura Pictures', 60000000.00, 145000000.00, 8.0, 'Australia');"""

insert_actor_movie_table = """INSERT INTO actor_movie (actor_id, movie_id, actor_movie_roles, actor_movie_notes) VALUES
    (1, 1, ARRAY['Hero', 'Adventurer'], 'Lead role in the movie.'),
    (2, 1, ARRAY['Detective'], 'Supporting role as the detective.'),
    (2, 2, ARRAY['Protagonist'], 'Main character in the story.'),
    (1, 2, ARRAY['Villain'], 'Antagonistic role in the movie.'),
    (3, 3, ARRAY['Lead', 'Singer'], 'Musical lead role in the film.'),
    (4, 4, ARRAY['Protagonist'], 'One of the main characters in the city drama.'),
    (1, 3, ARRAY['Dancer'], 'Featured role in the musical.'),
    (2, 3, ARRAY['Supporting'], 'Supporting role in the musical.');"""

cursor.execute(insert_person_table)
cursor.execute(insert_actor_table)
cursor.execute(insert_director_table)
cursor.execute(insert_movie_table)
cursor.execute(insert_actor_movie_table)

# query tables
print("\nAll persons:")
cursor.execute("SELECT person_firstname, person_lastname, person_birthdate, person_place_born, person_nationality, person_description FROM person")
for row in cursor.fetchall():
    print(row)

print("\nDistinct nationality:")
cursor.execute("SELECT DISTINCT person_nationality FROM person")
for row in cursor.fetchall():
    print(row)

print("\nMovies from US:")
cursor.execute("""SELECT movie_title, movie_about, movie_release_date, movie_release_country, movie_imdb FROM movie
                    WHERE movie_release_country = 'United States'""")
for row in cursor.fetchall():
    print(row)

print("\nMovies with IMDB score between 6 and 9:")
cursor.execute("""SELECT movie_title, movie_about, movie_release_date, movie_imdb FROM movie
                    WHERE movie_imdb >= 6 and movie_imdb <= 9""")
for row in cursor.fetchall():
    print(row)

print("\nPersons by nationality:")
cursor.execute("""SELECT person_nationality, COUNT(person_id) FROM person
                    GROUP BY person_nationality""")
for row in cursor.fetchall():
    print(row)

print("\nCountries making movies with average IMDB score above 8:")
cursor.execute("""SELECT movie_release_country, AVG(movie_imdb) FROM movie
                    GROUP BY movie_release_country
                    HAVING AVG(movie_imdb) >= 8""")
for row in cursor.fetchall():
    print(row)

print("\nMovies sorted descending by IMDB score:")
cursor.execute("""SELECT movie_title, movie_about, movie_release_date, movie_distributor, movie_imdb FROM movie
                    ORDER BY movie_imdb DESC""")
for row in cursor.fetchall():
    print(row)

print("\nTop 3 movies by IMDB score:")
cursor.execute("""SELECT movie_title, movie_about, movie_release_date, movie_distributor, movie_imdb FROM movie
                    LIMIT 3""")
for row in cursor.fetchall():
    print(row)

print("\nNext 3 movies by IMDB score:")
cursor.execute("""SELECT movie_title, movie_about, movie_release_date, movie_distributor, movie_imdb FROM movie
                    LIMIT 3 OFFSET 3""")
for row in cursor.fetchall():
    print(row)

# fetch table records
print("\nTop 3 movies by IMDB score:")
cursor.execute("BEGIN WORK")
cursor.execute("DECLARE cursor SCROLL CURSOR FOR SELECT * FROM movie")
cursor.execute("""FETCH FORWARD 3 FROM cursor""")
for row in cursor.fetchall():
    print(row)

print("\nPrevious movie in the TOP-3 by IMDB score:")
cursor.execute("""FETCH PRIOR FROM cursor""")
for row in cursor.fetchall():
    print(row)

cursor.execute("CLOSE cursor")
cursor.execute("COMMIT WORK")

# truncate tables
# cursor.execute("TRUNCATE actor_movie, movie, director, actor, person CASCADE")

cursor.close()
conn.close()
