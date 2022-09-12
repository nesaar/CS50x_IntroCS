select distinct d.name from directors a, movies b, ratings c, people d where a.movie_id = b.id and d.id = a.person_id and c.movie_id = b.id and c.rating >= 9.0;