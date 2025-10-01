from Includes.Dbh import Dbh

class Movies(Dbh):

    def _InsertMovie(self, title, genre, price, duration, rating, description, poster_path, status):

        # Setting Connection
        conn = self._connection()

        if not conn:
            print('Error connecting to database!...Parent Error(Movies)')
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
            print(f'Error inserting movie: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

    def _Get_movies(self):
        conn = self._connection()
        if not conn:
            print("Error connecting to database!...Parent Error(Movies)")
            return []

        cursor = conn.cursor(dictionary=True)  # dictionary=True so we get column names
        query = """
                SELECT movie_id, title, genre, price, duration, release_date, rating, description, poster_path, status
                FROM movies
                WHERE status = 'Available'
                ORDER BY release_date DESC
                LIMIT 4
                """


        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error fetching movies: {e}")
            return []
        finally:
            cursor.close()
            conn.close()