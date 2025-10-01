from Classes.Movies_Class import Movies

class MoviesCntrl(Movies):
    def __init__(self, title, genre, price, duration, rating, description, poster_path, status):
        super().__init__()  # init DB
        self.title = title
        self.genre = genre
        self.price = price
        self.duration = duration
        self.rating = rating
        self.description = description
        self.poster_path = poster_path
        self.status = status

    # --------------------------------- Save ---------------------------------------------------------
    def AddMovie(self):
        """Validate and insert movie into DB."""
        ok, errors = self.checkErrors()
        if not ok:
            print("Validation failed:", errors)
            return False

        result = self._InsertMovie(
            self.title,
            self.genre,
            self.price,
            self.duration,
            self.rating,
            self.description,
            self.poster_path,
            self.status
        )

        if result:
            print("✅ Movie saved successfully.")
            return True
        else:
            print("❌ Database insert failed.")
            return False

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
