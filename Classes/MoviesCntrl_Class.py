from Classes.Movies_Class import Movies

class MoviesCntrl(Movies):
    def __init__(self, title="", genre="", price=0, duration=0, rating="", description="", poster_path="", status="", movie_id=None):
        super().__init__()  # Initialize DB connection
        self.id = movie_id
        self.title = title
        self.genre = genre
        self.price = price
        self.duration = duration
        self.rating = rating
        self.description = description
        self.poster_path = poster_path
        self.status = status

    def AddMovie(self):
        """Validate and insert movie into DB."""
        ok, errors = self.checkErrors()
        if not ok:
            print("Validation failed:", errors)
            return False

        result = self._InsertMovie(
            self.title,
            self.genre,
            float(self.price),  # Ensure float for database
            int(self.duration),  # Ensure int for database
            self.rating,
            self.description,
            self.poster_path,
            self.status
        )
        if result:
            print(f"✅ Movie '{self.title}' inserted successfully.")
            return True
        else:
            print(f"❌ Failed to insert movie '{self.title}'.")
            return False

    def UpdateMovie(self):
        """Validate and update movie in DB."""
        if not self.id or not isinstance(self.id, int) or self.id <= 0:
            print("Validation failed: Invalid or missing movie ID.")
            return False

        ok, errors = self.checkErrors()
        if not ok:
            print("Validation failed:", errors)
            return False

        result = self._UpdateMovie(
            self.title,
            self.genre,
            float(self.price),  # Ensure float for database
            int(self.duration),  # Ensure int for database
            self.rating,
            self.description,
            self.poster_path,
            self.status,
            self.id
        )
        if result:
            print(f"✅ Movie with ID {self.id} ('{self.title}') updated successfully.")
            return True
        else:
            print(f"❌ Failed to update movie with ID {self.id} ('{self.title}').")
            return False

    def deleteMovie(self):
        """Delete a movie from the DB using its ID."""
        if not self.id or not isinstance(self.id, int) or self.id <= 0:
            print("Validation failed: Invalid or missing movie ID.")
            return False

        result = self._DeleteMovie(self.id)
        if result:
            print(f"✅ Movie with ID {self.id} deleted successfully.")
            return True
        else:
            print(f"❌ Failed to delete movie with ID {self.id}.")
            return False

    def checkErrors(self):
        """Run all validations before saving."""
        errors = {}

        if not isinstance(self.title, str) or not self.title.strip():
            errors["title"] = "Title is required and must be a string."
        if not isinstance(self.genre, str) or not self.genre.strip():
            errors["genre"] = "Genre is required and must be a string."
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            errors["price"] = "Price must be a positive number."
        if not isinstance(self.duration, (int, float)) or int(self.duration) <= 0:
            errors["duration"] = "Duration must be a positive integer."
        if not isinstance(self.rating, str) or not self.rating.strip():
            errors["rating"] = "Rating is required and must be a string."
        if not isinstance(self.status, str) or not self.status.strip():
            errors["status"] = "Status is required and must be a string."
        if not isinstance(self.description, str) or not self.description.strip():
            errors["description"] = "Description is required and must be a string."
        if not isinstance(self.poster_path, str) or not self.poster_path.strip():
            errors["poster"] = "Poster is required and must be a string."

        return (len(errors) == 0), errors