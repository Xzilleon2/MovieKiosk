from Includes.Dbh import Dbh

class Movies(Dbh):
    def _InsertMovie(self, title, genre, price, duration, rating, description, poster_path, status):
        # Basic input validation
        if not all([title, genre, price, duration, rating, status]):
            print("Error: Missing required fields for movie insertion")
            return False

        # Setting Connection
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False

        cursor = conn.cursor()
        query = ("INSERT INTO movies "
                 "(title, genre, price, duration, rating, description, poster_path, status) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        values = (title, genre, price, duration, rating, description, poster_path, status)

        try:
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting movie '{title}': {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def _UpdateMovie(self, title, genre, price, duration, rating, description, poster_path, status, movie_id):
        # Basic input validation
        if not all([title, genre, isinstance(price, (int, float)), isinstance(duration, (int, float)), rating, status,
                    description, poster_path]):
            print("Error: Missing or invalid required fields for movie update")
            return False

        # Ensure movie_id is valid
        if not isinstance(movie_id, int) or movie_id <= 0:
            print("Error: Invalid or missing movie ID")
            return False

        # Setting Connection
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False

        cursor = conn.cursor()
        query = """
                UPDATE movies
                SET title       = %s, \
                    genre       = %s, \
                    price       = %s, \
                    duration    = %s, \
                    rating      = %s,
                    description = %s, \
                    poster_path = %s, \
                    status      = %s
                WHERE movie_id = %s \
                """
        values = (title, genre, float(price), int(duration), rating, description, poster_path, status, movie_id)

        try:
            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount > 0:
                print(f"✅ Movie with ID {movie_id} updated successfully.")
                return True
            else:
                print(f"❌ No movie found with ID {movie_id}.")
                return False
        except Exception as e:
            print(f"Error updating movie '{title}': {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def _Get_movies(self):  # Renamed for consistency
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return []

        cursor = conn.cursor(dictionary=True)  # dictionary=True so we get column names
        query = """
                SELECT movie_id, title, genre, price, duration, release_date, rating, description, poster_path, status
                FROM movies
                ORDER BY release_date
                """  # Removed LIMIT and status filter for AdminPage

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

    def _DeleteMovie(self, movie_id):
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return False

        cursor = conn.cursor(dictionary=True)
        query = """
                DELETE FROM movies WHERE movie_id = %s
                """
        values = (movie_id,)  # Use tuple for single parameter

        try:
            cursor.execute(query, values)
            conn.commit()  # Commit the transaction
            return cursor.rowcount > 0  # Return True if at least one row was deleted
        except Exception as e:
            print(f"Error deleting movie with ID {movie_id}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()