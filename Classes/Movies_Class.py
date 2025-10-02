from Includes.Dbh import Dbh
from datetime import datetime, timedelta

class Movies(Dbh):
    def get_all_movies(self):
        """Fetch all movies from the Movies table."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT movie_id, title, genre, price, duration, release_date, rating, description, poster_path, status
            FROM Movies
            ORDER BY release_date
        """

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results if results else []
        except Exception as e:
            print(f"Error fetching movies: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_movies_this_month(self, limit=4):
        """Fetch movies with showtimes in the current month, limited to the specified number."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return []

        cursor = conn.cursor(dictionary=True)
        # Get the start and end of the current month
        current_date = datetime(2025, 10, 3, 1, 32)  # Current date: 01:32 AM PST, Oct 03, 2025
        start_of_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (start_of_month.replace(month=start_of_month.month % 12 + 1)
                     if start_of_month.month < 12 else start_of_month.replace(year=start_of_month.year + 1, month=1))
        end_of_month = next_month - timedelta(seconds=1)

        query = """
            SELECT DISTINCT m.movie_id, m.title, m.genre, m.price, m.duration, m.release_date, 
                           m.rating, m.description, m.poster_path, m.status
            FROM Movies m
            JOIN Showtimes s ON m.movie_id = s.movie_id
            WHERE s.start_time >= %s AND s.start_time <= %s
            ORDER BY m.release_date
            LIMIT %s
        """
        values = (start_of_month, end_of_month, limit)

        try:
            cursor.execute(query, values)
            results = cursor.fetchall()
            return results if results else []
        except Exception as e:
            print(f"Error fetching movies for this month: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def _InsertMovie(self, title, genre, price, duration, rating, description, poster_path, status):
        """Insert a movie into the Movies table and return the inserted movie_id."""
        if not all([title, genre, price, duration, rating, status, description, poster_path]):
            print("Error: Missing required fields for movie insertion")
            return False, None

        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False, None

        cursor = conn.cursor()
        query = """
            INSERT INTO Movies 
            (title, genre, price, duration, rating, description, poster_path, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (title, genre, float(price), int(duration), rating, description, poster_path, status)

        try:
            cursor.execute(query, values)
            conn.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            movie_id = cursor.fetchone()[0]
            return True, movie_id
        except Exception as e:
            print(f"Error inserting movie '{title}': {e}")
            return False, None
        finally:
            cursor.close()
            conn.close()

    def _UpdateMovie(self, title, genre, price, duration, rating, description, poster_path, status, movie_id):
        """Update a movie in the Movies table."""
        if not all([title, genre, isinstance(price, (int, float)), isinstance(duration, (int, float)), rating, status, description, poster_path]):
            print("Error: Missing or invalid required fields for movie update")
            return False

        if not isinstance(movie_id, int) or movie_id <= 0:
            print("Error: Invalid or missing movie ID")
            return False

        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False

        cursor = conn.cursor()
        query = """
            UPDATE Movies
            SET title = %s, genre = %s, price = %s, duration = %s, rating = %s,
                description = %s, poster_path = %s, status = %s
            WHERE movie_id = %s
        """
        values = (title, genre, float(price), int(duration), rating, description, poster_path, status, movie_id)

        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating movie '{title}': {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def _DeleteMovie(self, movie_id):
        """Delete a movie from the Movies table."""
        if not isinstance(movie_id, int) or movie_id <= 0:
            print("Error: Invalid or missing movie ID")
            return False

        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False

        cursor = conn.cursor()
        query = "DELETE FROM Movies WHERE movie_id = %s"
        values = (movie_id,)

        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting movie with ID {movie_id}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def _InsertShowtime(self, movie_id, gate_id, start_time, end_time, available_seats):
        """Insert a showtime record into the Showtimes table."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False

        cursor = conn.cursor()
        query = """
            INSERT INTO Showtimes (movie_id, gate_id, start_time, end_time, available_seats)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (movie_id, gate_id, start_time, end_time, available_seats)

        try:
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting showtime for movie ID {movie_id}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def _GetAvailableGate(self):
        """Find the gate with the most available seats."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return None

        cursor = conn.cursor()
        query = """
            SELECT g.gate_id, g.total_seat_capacity - COALESCE(SUM(s.available_seats), 0) as available_seats
            FROM CinemaGates g
            LEFT JOIN Showtimes s ON g.gate_id = s.gate_id
            GROUP BY g.gate_id
            HAVING available_seats > 0
            ORDER BY available_seats DESC LIMIT 1
        """

        try:
            cursor.execute(query)
            gate = cursor.fetchone()
            return gate[0] if gate else None
        except Exception as e:
            print(f"Error fetching available gate: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def _GetGateCapacity(self, gate_id):
        """Fetch the total seat capacity for a given gate."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return 0

        cursor = conn.cursor()
        query = "SELECT total_seat_capacity FROM CinemaGates WHERE gate_id = %s"
        cursor.execute(query, (gate_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else 0

    def _IsGateAvailableForMonth(self, gate_id, start_date, end_date):
        """Check if the gate is available for the specified month."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False

        cursor = conn.cursor()
        query = """
            SELECT COUNT(*) 
            FROM Showtimes 
            WHERE gate_id = %s 
            AND start_time >= %s 
            AND start_time <= %s
        """
        values = (gate_id, start_date, end_date)

        try:
            cursor.execute(query, values)
            count = cursor.fetchone()[0]
            return count == 0
        except Exception as e:
            print(f"Error checking gate availability: {e}")
            return False
        finally:
            cursor.close()
            conn.close()