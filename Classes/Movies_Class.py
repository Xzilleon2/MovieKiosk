from Includes.Dbh import Dbh
from datetime import datetime, timedelta

class Movies(Dbh):
    def _get_movies_this_month(self, limit=None):
        """Fetch movies with showtimes in the current month, optionally limited."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return []

        cursor = conn.cursor(dictionary=True)
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = (start_date + timedelta(days=31)).replace(day=1)

        query = """
            SELECT m.movie_id, m.title, m.genre, m.price, m.duration, m.release_date, 
                   m.rating, m.description, m.poster_path, m.status
            FROM Movies m
            JOIN Showtimes s ON m.movie_id = s.movie_id
            WHERE s.start_time >= %s AND s.start_time < %s
            GROUP BY m.movie_id
        """
        values = (start_date, end_date)

        if limit is not None:
            query += " LIMIT %s"
            values = values + (limit,)

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

    def _get_movies_next_month(self, limit=None):
        """Fetch movies with showtimes for the next month."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            current_date = datetime.now().date()
            # Start of next month
            start_date = (current_date.replace(day=1) + timedelta(days=31)).replace(day=1)
            # End of next month
            end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            query = """
            SELECT m.movie_id, m.title, m.genre, m.price, m.duration, m.release_date, 
                   m.rating, m.description, m.poster_path, m.status
            FROM Movies m
            JOIN Showtimes s ON m.movie_id = s.movie_id
            WHERE s.start_time >= %s AND s.start_time < %s
            GROUP BY m.movie_id
            """
            if limit:
                query += " LIMIT %s"
                cursor.execute(query, (start_date, end_date, limit))
            else:
                cursor.execute(query, (start_date, end_date))
            movies = cursor.fetchall()
            for movie in movies:
                movie['price'] = float(movie['price']) if movie['price'] is not None else 0.0
                movie['duration'] = int(movie['duration']) if movie['duration'] is not None else 0
            print(f"Retrieved {len(movies)} movies for {start_date} to {end_date}")
            return movies
        except Exception as e:
            print(f"Error fetching movies for next month: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def _get_available_showtimes(self, movie_id, date=None):
        """Fetch all showtimes for a movie scheduled today (current date)."""
        conn = self._connection()
        if not conn:
            print("❌ Error connecting to database!...Parent Error(Movies)")
            return []

        cursor = conn.cursor(dictionary=True)
        today = datetime.now().date() if date is None else date
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)

        query = """
                SELECT s.showtime_id,
                       s.gate_id,
                       g.name AS gate_name, TIME (s.start_time) AS start_time, TIME (s.end_time) AS end_time, s.available_seats
                FROM Showtimes s
                    JOIN CinemaGates g \
                ON s.gate_id = g.gate_id
                WHERE s.movie_id = %s
                  AND s.start_time BETWEEN %s \
                  AND %s
                ORDER BY g.name, s.start_time \
                """
        values = (movie_id, start_of_day, end_of_day)

        try:
            cursor.execute(query, values)
            results = cursor.fetchall()
            print(f"[DEBUG] Found {len(results)} showtimes for {today} (movie {movie_id})")
            return results
        except Exception as e:
            print(f"❌ Error fetching showtimes for movie ID {movie_id}: {e}")
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

    def _GetMovies(self):
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
            AND start_time < %s
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

    def _IsGateValid(self, gate_id):
        """Check if a gate ID is valid."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False

        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM CinemaGates WHERE gate_id = %s"
        values = (gate_id,)

        try:
            cursor.execute(query, values)
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Error validating gate ID {gate_id}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_available_gates(self):
        """Fetch available gates."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT gate_id, name, total_seat_capacity FROM CinemaGates ORDER BY gate_id"

        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results if results else []
        except Exception as e:
            print(f"Error fetching gates: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def check_seat_availability(self, showtime_id, seat):
        """Check if a specific seat is available for a given showtime."""
        conn = self._connection()
        if not conn:
            print("❌ Error connecting to database!...Parent Error(Movies)")
            return False

        try:
            with conn.cursor() as cursor:
                query = """
                        SELECT COUNT(*)
                        FROM Tickets
                        WHERE showtime_id = %s \
                          AND seat = %s \
                        """
                cursor.execute(query, (showtime_id, seat))
                result = cursor.fetchone()
                count = result[0] if result else 0
                return count == 0
        except Exception as e:
            print(f"⚠️ Error checking seat availability for showtime ID {showtime_id}: {e}")
            return False
        finally:
            conn.close()

    def book_seat(self, showtime_id, seat):
        """Book a seat for a showtime."""
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False

        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO Tickets (showtime_id, seat, purchase_time)
                VALUES (%s, %s, %s)
            """
            values = (showtime_id, seat, datetime.now())
            cursor.execute(query, values)

            query = """
                UPDATE Showtimes SET available_seats = available_seats - 1
                WHERE showtime_id = %s AND available_seats > 0
            """
            cursor.execute(query, (showtime_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error booking seat for showtime ID {showtime_id}: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def _get_available_seats(self, showtime_id, gate_name):
        conn = self._connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                            SELECT * FROM seats s
                            WHERE s.gate_id =  %s AND showtime_id = %s AND status = "Available"
                           """, (gate_name, showtime_id))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
