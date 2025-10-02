from Classes.Movies_Class import Movies
from datetime import datetime, timedelta

class MoviesCntrl:
    def __init__(self, title="", genre="", price=0, duration=0, release_date=None, rating="", description="", poster_path="", status="", movie_id=None, gate=None):
        self.model = Movies()
        self.id = movie_id
        self.gate = gate
        self.title = title
        self.genre = genre
        self.price = price
        self.duration = duration
        self.release_date = release_date
        self.rating = rating
        self.description = description
        self.poster_path = poster_path
        self.status = status

    def AddMovie(self):
        """Validate and add a movie, scheduling it for a month with 4 specific time slots."""
        ok, errors = self.checkErrors()
        if not ok:
            print("Validation failed:", errors)
            return False, errors

        success, movie_id = self.model._InsertMovie(
            self.title, self.genre, float(self.price), int(self.duration),
            self.rating, self.description, self.poster_path, self.status
        )
        if not success:
            print(f"❌ Failed to insert movie '{self.title}'.")
            return False, ["Failed to insert movie."]

        print(f"✅ Movie '{self.title}' inserted successfully with ID {movie_id}.")

        gate_id = None
        if self.gate:
            try:
                # Handle both "Gate X (Gate X)" and direct integer string
                gate_str = self.gate
                if "Gate" in gate_str:
                    gate_id = int(gate_str.split(" ")[1].strip("()"))  # e.g., "Gate 1 (Gate 1)" -> "1"
                else:
                    gate_id = int(gate_str)  # Direct integer string, e.g., "1"
                if not self.model._IsGateValid(gate_id):
                    print(f"❌ Invalid gate ID {gate_id}. No such gate exists in CinemaGates.")
                    return False, [f"Invalid gate ID {gate_id}."]
            except (ValueError, IndexError) as e:
                print(f"❌ Invalid gate ID format: {self.gate}, error: {e}")
                return False, [f"Invalid gate ID format: {self.gate}."]
        else:
            gate_id = self.model._GetAvailableGate()
            if not gate_id:
                print("❌ No available gates for assignment. Please add gates to CinemaGates.")
                return False, ["No available gates for assignment."]

        try:
            start_date = datetime.strptime(self.release_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
        except (ValueError, TypeError):
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        end_date = start_date + timedelta(days=30)
        if not self.model._IsGateAvailableForMonth(gate_id, start_date, end_date):
            print(f"❌ Gate {gate_id} is not available for the entire month.")
            return False, [f"Gate {gate_id} is not available for the entire month."]

        showtimes_per_day = [10, 14, 18, 22]  # 10:00 AM, 2:00 PM, 6:00 PM, 10:00 PM
        available_seats = 30
        for day in range(30):
            for hour in showtimes_per_day:
                start_time = start_date.replace(hour=hour) + timedelta(days=day)
                end_time = start_time + timedelta(minutes=int(self.duration) + 15)
                if not self.model._InsertShowtime(movie_id, gate_id, start_time, end_time, available_seats):
                    print(f"❌ Failed to schedule showtime for '{self.title}' on {start_time} at Gate {gate_id}.")
                    return False, [f"Failed to schedule showtime on {start_time}."]
                print(f"Scheduled showtime for '{self.title}' on {start_time} at Gate {gate_id}.")

        print(f"✅ Movie '{self.title}' assigned to Gate {gate_id} for 30 days with 4 daily showtimes.")
        return True, []

    def checkErrors(self):
        """Validate movie input data."""
        errors = {}
        if not self.title:
            errors["title"] = "Title is required."
        if not self.genre:
            errors["genre"] = "Genre is required."
        try:
            if float(self.price) <= 0:
                errors["price"] = "Price must be a positive number."
        except (ValueError, TypeError):
            errors["price"] = "Price must be a number."
        try:
            if int(self.duration) <= 0:
                errors["duration"] = "Duration must be a positive number."
        except (ValueError, TypeError):
            errors["duration"] = "Duration must be a number."
        if not self.rating:
            errors["rating"] = "Rating is required."
        if not self.description:
            errors["description"] = "Description is required."
        if not self.poster_path:
            errors["poster"] = "Poster is required."
        if not self.status:
            errors["status"] = "Status is required."
        if self.release_date:
            try:
                datetime.strptime(self.release_date, "%Y-%m-%d")
            except (ValueError, TypeError):
                errors["release_date"] = "Release date must be in YYYY-MM-DD format."
        else:
            errors["release_date"] = "Release date is required."
        return len(errors) == 0, errors

    def UpdateMovie(self):
        """Update an existing movie."""
        ok, errors = self.checkErrors()
        if not ok:
            print("Validation failed:", errors)
            return False

        if not self.id or not isinstance(self.id, int) or self.id <= 0:
            print("Invalid movie ID.")
            return False

        success = self.model._UpdateMovie(
            self.id, self.title, self.genre, float(self.price), int(self.duration),
            self.rating, self.description, self.poster_path, self.status
        )
        if not success:
            print(f"❌ Failed to update movie '{self.title}'.")
            return False

        print(f"✅ Movie '{self.title}' updated successfully.")
        return True

    def deleteMovie(self, movie_id):
        """Delete a movie and its showtimes."""
        success = self.model._DeleteMovie(movie_id)
        if not success:
            print(f"❌ Failed to delete movie ID {movie_id}.")
            return False
        print(f"✅ Movie ID {movie_id} deleted successfully.")
        return True

    def get_movies_this_month(self, limit=None):
        """Fetch movies with showtimes for the current month."""
        movies = self.model.get_movies_this_month(limit)
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

    def get_available_gates(self):
        """Fetch available gates."""
        return self.model.get_available_gates()

    def get_available_showtimes(self, movie_id, date=None):
        """Fetch available showtimes for a movie."""
        showtimes = self.model.get_available_showtimes(movie_id, date)
        return [
            {
                "showtime_id": s["showtime_id"],
                "gate_id": s["gate_id"],
                "gate_name": s["gate_name"],
                "start_time": s["start_time"].strftime("%I:%M %p"),
                "end_time": s["end_time"].strftime("%I:%M %p"),
                "available_seats": s["available_seats"]
            }
            for s in showtimes
        ]

    def check_seat_availability(self, showtime_id, seat):
        """Check if a seat is available for a showtime."""
        return self.model.check_seat_availability(showtime_id, seat)

    def book_seat(self, showtime_id, seat):
        """Book a seat for a showtime."""
        return self.model.book_seat(showtime_id, seat)