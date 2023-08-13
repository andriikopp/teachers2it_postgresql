-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


DROP TABLE IF EXISTS public.actor;

CREATE TABLE IF NOT EXISTS public.actor
(
    actor_id integer NOT NULL,
    actor_height_meters numeric(3, 2) NOT NULL,
    CONSTRAINT actor_pkey PRIMARY KEY (actor_id)
);

DROP TABLE IF EXISTS public.actor_movie;

CREATE TABLE IF NOT EXISTS public.actor_movie
(
    actor_id integer NOT NULL,
    movie_id integer NOT NULL,
    actor_movie_roles character varying(100)[] COLLATE pg_catalog."default" NOT NULL,
    actor_movie_notes text COLLATE pg_catalog."default",
    CONSTRAINT actor_movie_pkey PRIMARY KEY (actor_id, movie_id)
);

DROP TABLE IF EXISTS public.director;

CREATE TABLE IF NOT EXISTS public.director
(
    director_id integer NOT NULL,
    CONSTRAINT director_pkey PRIMARY KEY (director_id)
);

DROP TABLE IF EXISTS public.movie;

CREATE TABLE IF NOT EXISTS public.movie
(
    movie_id integer NOT NULL DEFAULT nextval('movie_movie_id_seq'::regclass),
    movie_title character varying(150) COLLATE pg_catalog."default" NOT NULL,
    movie_about text COLLATE pg_catalog."default" NOT NULL,
    movie_release_date date NOT NULL,
    director_id integer NOT NULL,
    movie_distributor character varying(50) COLLATE pg_catalog."default" NOT NULL,
    movie_budget_usd numeric(18, 2) NOT NULL,
    movie_boxoffice_usd numeric(18, 2) NOT NULL,
    movie_imdb numeric(3, 1) NOT NULL,
    movie_release_country character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT movie_pkey PRIMARY KEY (movie_id)
);

DROP TABLE IF EXISTS public.person;

CREATE TABLE IF NOT EXISTS public.person
(
    person_id integer NOT NULL DEFAULT nextval('person_person_id_seq'::regclass),
    person_firstname character varying(50) COLLATE pg_catalog."default" NOT NULL,
    person_lastname character varying(50) COLLATE pg_catalog."default" NOT NULL,
    person_birthdate date NOT NULL,
    person_deathdate date,
    person_place_born character varying(100) COLLATE pg_catalog."default" NOT NULL,
    person_nationality character varying(100) COLLATE pg_catalog."default" NOT NULL,
    person_description text COLLATE pg_catalog."default",
    CONSTRAINT person_pkey PRIMARY KEY (person_id)
);

ALTER TABLE IF EXISTS public.actor
    ADD CONSTRAINT actor_actor_id_fkey FOREIGN KEY (actor_id)
    REFERENCES public.person (person_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS actor_pkey
    ON public.actor(actor_id);


ALTER TABLE IF EXISTS public.actor_movie
    ADD CONSTRAINT actor_movie_actor_id_fkey FOREIGN KEY (actor_id)
    REFERENCES public.actor (actor_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.actor_movie
    ADD CONSTRAINT actor_movie_movie_id_fkey FOREIGN KEY (movie_id)
    REFERENCES public.movie (movie_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.director
    ADD CONSTRAINT director_director_id_fkey FOREIGN KEY (director_id)
    REFERENCES public.person (person_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS director_pkey
    ON public.director(director_id);


ALTER TABLE IF EXISTS public.movie
    ADD CONSTRAINT movie_director_id_fkey FOREIGN KEY (director_id)
    REFERENCES public.director (director_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;