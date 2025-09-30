from Classes import Movies  # your model
import datetime

class MoviesCntrl_Class(Movies):
    def __init__(self, title, genre, price, duration, rating, description, poster_path):
        super().__init__()  # init parent (Dbh)
        self.title = title
        self.genre = genre
        self.price = price
        self.duration = duration
        self.rating = rating
        self.description = description
        self.poster_path = poster_path

    # (keep your existing validation methods...)

    def save(self):
        """Validate and insert movie into DB."""
        ok, errors = self.checkErrors()
        if not ok:
            return False, errors

        result = self._InsertMovie(
            self.title,
            self.genre,
            self.price,
            self.duration,
            self.rating,
            self.description,
            self.poster_path
        )

        if result:
            return True, {}
        else:
            return False, {"db": ["Database insert failed."]}
