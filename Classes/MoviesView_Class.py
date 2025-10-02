from Classes.MoviesCntrl_Class import Movies

class MoviesView(Movies):
    def getMoviesThisMonth(self):
        """
        Fetch available movies created this month (limit 4).
        Returns a list of dictionaries.
        """
        movies = self._Get_movies()

        if not movies:
            return []

        result = []
        for movie in movies:
            result.append({
                "id": movie["movie_id"],
                "title": movie["title"],
                "genre": movie["genre"],
                "price": movie['price'],
                "duration": movie['duration'],
                "date": movie["release_date"].strftime("%B %d, %Y"),
                "rating": movie["rating"],
                "description": movie["description"],
                "poster": movie["poster_path"],
                "status": movie["status"],
            })
        return result
