from Classes import Movies_Class
import datetime

class MoviesCntrl_Class(Movies_Class):
    def __init__(self, title, genre, price, duration, rating, status, description, poster_path):
        super().__init__()  # init DB
        self.title = title
        self.genre = genre
        self.price = price
        self.duration = duration
        self.rating = rating
        self.status = status
        self.description = description
        self.poster_path = poster_path

        # Store messages (like PHP $error / $success)
        self.message = ""
        self.errors = {}

    # --------------------------------- Save ---------------------------------------------------------
    def save(self):
        """Validate and insert movie into DB."""
        ok, errors = self.checkErrors()
        if not ok:
            self.errors = errors
            self.message = "Validation failed. Please check the form. (Controller)"
            return False, errors

        result = self._InsertMovie(
            self.title,
            self.genre,
            self.price,
            self.duration,
            self.rating,
            self.status,
            self.description,
            self.poster_path
        )

        if result:
            self.message = "Movie saved successfully ✅"
            return True, {}
        else:
            self.errors = {"db": ["Database insert failed. (Controller)"]}
            self.message = "Database insert failed. (Controller)"
            return False, self.errors

    # --------------------------------- Error Handling -------------------------------------------------------
    def checkErrors(self):
        """Run all validations before saving."""
        errors = {}

        if not self.title.strip():
            errors["title"] = "Title is required."
        if not self.genre.strip():
            errors["genre"] = "Genre is required."
        if not self.price or not str(self.price).isdigit():
            errors["price"] = "Price must be a number."
        if not self.duration or not str(self.duration).isdigit():
            errors["duration"] = "Duration must be a number."
        if not self.rating.strip():
            errors["rating"] = "Rating is required."
        if not self.status.strip():
            errors["status"] = "Status is required."
        if not self.description.strip():
            errors["description"] = "Description is required."
        if not self.poster_path.strip():
            errors["poster"] = "Poster is required."

        return (len(errors) == 0), errors
