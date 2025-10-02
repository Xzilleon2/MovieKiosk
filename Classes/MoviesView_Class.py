from Classes.MoviesCntrl_Class import MoviesCntrl

class MoviesView:
    def __init__(self):
        self.controller = MoviesCntrl()

    def getMoviesThisMonth(self):
        """
        Fetch available movies with showtimes in the current month (limit 4).
        Returns a list of dictionaries.
        """
        return self.controller.get_movies_this_month(limit=4)