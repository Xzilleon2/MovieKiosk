from Classes.Movies_Class import Movies
from datetime import datetime, timedelta

class MoviesCntrl:
    def __init__(self, title="", genre="", price=0, duration=0, rating="", description="", poster_path="", status="", movie_id=None, gate=None):
        self.model = Movies()
        self.id = movie_id
        self.gate = gate
        self.title = title
        self.genre = genre
        self.price = price
        self.duration = duration
        self.rating = rating
        self.description = description
        self.poster_path = poster_path
        self.status = status

    def AddMovie(self):
        """Validate and add a movie, scheduling it for a month."""
        ok, errors = self.checkErrors()
        if not ok:
            print("Validation failed:", errors)
            return False

        success, movie_id = self.model._InsertMovie(
            self.title,
            self.genre,
            float(self.price),
            int(self.duration),
            self.rating,
            self.description,
            self.poster_path,
            self.status
        )
        if not success:
            print(f"❌ Failed to insert movie '{self.title}'.")
            return False

        print(f"✅ Movie '{self.title}' inserted successfully with ID {movie_id}.")

        gate_id = int(self.gate) if self.gate else self.model._GetAvailableGate()
        if not gate_id:
            print("❌ No available gates for assignment.")
            return False

        start_date = datetime(2025, 10, 3, 1, 32).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        end_date = start_date + timedelta(days=30)
        if not self.model._IsGateAvailableForMonth(gate_id, start_date, end_date):
            print(f"❌ Gate {gate_id} is not available for the entire month.")
            return False

        showtimes_per_day = [10, 14, 18]
        available_seats = self.model._GetGateCapacity(gate_id)
        start_date = start_date.replace(hour=10, minute=0)

        for day in range(30):
            for hour in showtimes_per_day:
                start_time = start_date.replace(hour=hour) + timedelta(days=day)
                end_time = start_time + timedelta(minutes=int(self.duration) + 15)
                if not self.model._InsertShowtime(movie_id, gate_id, start_time, end_time, available_seats):
                    print(f"❌ Failed to schedule showtime for '{self.title}' on {start_time} at Gate {gate_id}.")
                    return False

        print(f"✅ Movie '{self.title}' assigned to Gate {gate_id} for 30 days with {len(showtimes_per_day)} daily showtimes.")
        return True

    def UpdateMovie(self):
        """Validate and update a movie."""
        if not self.id or not isinstance(self.id, int) or self.id <= 0:
            print("Validation failed: Invalid or missing movie ID.")
            return False

        ok, errors = self.checkErrors()
        if not ok:
            print("Validation failed:", errors)
            return False

        result = self.model._UpdateMovie(
            self.title,
            self.genre,
            float(self.price),
            int(self.duration),
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
        """Delete a movie using its ID."""
        if not self.id or not isinstance(self.id, int) or self.id <= 0:
            print("Validation failed: Invalid or missing movie ID.")
            return False

        result = self.model._DeleteMovie(self.id)
        if result:
            print(f"✅ Movie with ID {self.id} deleted successfully.")
            return True
        else:
            print(f"❌ Failed to delete movie with ID {self.id}.")
            return False

    def get_movies_this_month(self, limit=4):
        """Fetch movies with showtimes in the current month."""
        movies = self.model.get_movies_this_month(limit)
        if not movies:
            return []

        result = []
        for movie in movies:
            result.append({
                "id": movie["movie_id"],
                "title": movie["title"],
                "genre": movie["genre"],
                "price": movie["price"],
                "duration": movie["duration"],
                "date": movie["release_date"].strftime("%B %d, %Y") if movie["release_date"] else "N/A",
                "rating": movie["rating"],
                "description": movie["description"],
                "poster": movie["poster_path"],
                "status": movie["status"],
            })
        return result

    def checkErrors(self):
        """Validate movie attributes."""
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