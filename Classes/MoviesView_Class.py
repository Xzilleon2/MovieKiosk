from Classes import Movies_Class
from Includes import Dbh

class MoviesView(Movies_Class):

    # View all Movies
    def showMovies(self, title=None):
        """
        Fetch and display movies.
        If a title is given, show only matching movies,
        otherwise show all movies.
        """
        if title:
            movies = self._getMovies(title)
        else:
            movies = self._getAllMovies()

        if not movies:
            print("No movies found.")
            return

        print("=== Movies ===")
        for movie in movies:
            print(f"ID: {movie['movie_id']}")
            print(f"Title: {movie['title']}")
            print(f"Genre: {movie['genre']}")
            print(f"Price: {movie['price']}")
            print(f"Duration: {movie['duration']} mins")
            print(f"Rating: {movie['rating']}")
            print(f"Description: {movie['description']}")
            print(f"Poster Path: {movie['poster_path']}")
            print("-" * 30)
