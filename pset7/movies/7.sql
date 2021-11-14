SELECT rating, title FROM ratings
JOIN movies
ON movies.id = ratings.movie_id
WHERE movies.year = 2010
ORDER BY rating DESC, title ASC;