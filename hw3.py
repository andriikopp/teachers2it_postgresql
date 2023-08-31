import psycopg2

conn = psycopg2.connect(
    dbname="movies",
    user="postgres",
    password="admin",
    host="127.0.0.1"
)

cursor = conn.cursor()
conn.autocommit = True

# joins
print("\nActors with the height:")
cursor.execute("""SELECT person_firstname, person_lastname, person_birthdate, person_place_born, person_nationality, person_description, actor_height_meters 
                    FROM person INNER JOIN actor ON (person.person_id = actor.actor_id)""")
for row in cursor.fetchall():
    print(row)

print("\nActors, movies, and roles:")
cursor.execute("""SELECT person_firstname, person_lastname, movie_title, movie_release_date, actor_movie_roles, actor_movie_notes 
                    FROM person INNER JOIN actor_movie ON (person.person_id = actor_movie.actor_id) 
                        INNER JOIN movie ON (movie.movie_id = actor_movie.movie_id)""")
for row in cursor.fetchall():
    print(row)

print("\nMovies and directors:")
cursor.execute("""SELECT person_firstname, person_lastname, movie_title, movie_release_date, movie_budget_usd, movie_boxoffice_usd, movie_imdb, movie_release_country 
                    FROM person INNER JOIN movie ON (person.person_id = movie.director_id)""")
for row in cursor.fetchall():
    print(row)

print("\nDirectors who did not film a single movie:")
cursor.execute("""SELECT person_firstname, person_lastname, movie_title, movie_release_date, movie_budget_usd, movie_boxoffice_usd, movie_imdb, movie_release_country 
                    FROM person LEFT JOIN movie ON (person.person_id = movie.director_id) 
                    WHERE movie.director_id IS NULL""")
for row in cursor.fetchall():
    print(row)

print("\nActors who did not play in a single movie:")
cursor.execute("""SELECT person_firstname, person_lastname, actor_movie_roles, actor_movie_notes 
                    FROM actor_movie RIGHT JOIN person ON (actor_movie.actor_id = person.person_id) 
                    WHERE actor_movie.actor_id IS NULL""")
for row in cursor.fetchall():
    print(row)

# union
print("\nActors and directors without movies:")
cursor.execute("""SELECT person_firstname, person_lastname, person_birthdate, person_nationality, 'Director' 
                    FROM person LEFT JOIN movie ON (person.person_id = movie.director_id) 
                    WHERE movie.director_id IS NULL 
                    UNION
                    SELECT person_firstname, person_lastname, person_birthdate, person_nationality, 'Actor' 
                    FROM actor_movie RIGHT JOIN person ON (actor_movie.actor_id = person.person_id) 
                    WHERE actor_movie.actor_id IS NULL""")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
