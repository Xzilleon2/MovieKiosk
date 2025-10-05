from Classes.MoviesCntrl_Class import MoviesCntrl

class MoviesView:
    def __init__(self):
        self.controller = MoviesCntrl()

    def __get_movies_this_month(self, limit=None):
        """Fetch movies with showtimes for the current month."""
        movies = self.controller.model._get_movies_this_month(limit)
        return [
            {
                "id": movie["movie_id"],
                "title": movie["title"],
                "genre": movie["genre"],
                "price": float(movie["price"]) if movie["price"] is not None else 0.0,
                "duration": int(movie["duration"]) if movie["duration"] is not None else 0,
                "date": movie["release_date"].strftime("%B %d, %Y"),
                "rating": movie["rating"],
                "description": movie["description"],
                "poster": movie["poster_path"],
                "status": movie["status"]
            }
            for movie in movies
        ]

    def __get_movies_next_month(self, limit=None):
        """Fetch movies with showtimes for the current month."""
        movies = self.controller.model._get_movies_next_month(limit)
        return [
            {
                "id": movie["movie_id"],
                "title": movie["title"],
                "genre": movie["genre"],
                "price": float(movie["price"]) if movie["price"] is not None else 0.0,
                "duration": int(movie["duration"]) if movie["duration"] is not None else 0,
                "date": movie["release_date"].strftime("%B %d, %Y"),
                "rating": movie["rating"],
                "description": movie["description"],
                "poster": movie["poster_path"],
                "status": movie["status"]
            }
            for movie in movies
        ]

    def getMoviesThisMonth(self):
        """
        Fetch available movies with showtimes in the current month (limit 4).
        Returns a list of dictionaries.
        """
        return self.__get_movies_this_month(limit=4)

    def getMoviesNextMonth(self):
        """
        Fetch available movies with showtimes in the current month (limit 4).
        Returns a list of dictionaries.
        """
        return self.__get_movies_next_month(limit=4)
