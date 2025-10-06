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

    def insert_ticket(self):
        pass

    def book_seat(self, showtime_id, seat):
        """Book a seat for a showtime."""
        return self.model.book_seat(showtime_id, seat)

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

    def get_available_showtimes(self, movie_id, date):
        showtimes = self.model._get_available_showtimes(movie_id, date)
        formatted_showtimes = []

        for s in showtimes:
            start_val = s["start_time"]
            end_val = s["end_time"]

            # ✅ Convert timedelta → time → formatted string
            if isinstance(start_val, timedelta):
                total_seconds = int(start_val.total_seconds())
                hours = (total_seconds // 3600) % 24
                minutes = (total_seconds // 60) % 60
                start_str = f"{hours % 12 or 12}:{minutes:02d} {'AM' if hours < 12 else 'PM'}"
            elif isinstance(start_val, datetime):
                start_str = start_val.strftime("%I:%M %p")
            else:
                start_str = str(start_val)

            if isinstance(end_val, timedelta):
                total_seconds = int(end_val.total_seconds())
                hours = (total_seconds // 3600) % 24
                minutes = (total_seconds // 60) % 60
                end_str = f"{hours % 12 or 12}:{minutes:02d} {'AM' if hours < 12 else 'PM'}"
            elif isinstance(end_val, datetime):
                end_str = end_val.strftime("%I:%M %p")
            else:
                end_str = str(end_val)

            formatted_showtimes.append({
                "showtime_id": s["showtime_id"],
                "gate_id": s["gate_id"],
                "gate_name": s["gate_name"],
                "start_time": start_str,
                "end_time": end_str,
                "available_seats": s["available_seats"]
            })

        return formatted_showtimes

    def get_gate_id_by_name(self, gate_name):
        """Return the gate_id for a given gate name."""
        try:
            conn = self.model._connection()
            if not conn:
                print("❌ Database connection failed in get_gate_id_by_name()")
                return None

            cursor = conn.cursor(dictionary=True)
            query = "SELECT gate_id FROM CinemaGates WHERE name = %s LIMIT 1"
            cursor.execute(query, (gate_name,))
            result = cursor.fetchone()

            if result:
                return result["gate_id"]
            else:
                print(f"⚠️ No gate found with name '{gate_name}'")
                return None

        except Exception as e:
            print(f"❌ Error in get_gate_id_by_name(): {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_available_gates(self):
        """Fetch available gates."""

        return self.model.get_available_gates()

    def check_seat_availability(self, showtime_id, seat):
        """Check if a seat is available for a showtime."""
        return self.model.check_seat_availability(showtime_id, seat)

    def get_available_seats(self, showtime_id, gate_name):
        return self.model._get_available_seats(showtime_id, gate_name)
