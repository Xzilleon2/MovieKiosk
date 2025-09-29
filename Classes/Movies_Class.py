from Includes import Dbh

class Movies(Dbh):

    def _InsertMovie(self, title, genre, price, duration, rating, description, poster_path):

        # Setting Connection
        conn = self._connection()

        if not conn:
            print('Error connecting to database!')
            return False

        cursor = conn.cursor()
        query = ("INSERT INTO Movies (title, genre, price, duration, rating, description, poster_path) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        values = (title, genre, price, duration, rating, description, poster_path)

        try:
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print('Error inserting movie: {}'.format(e))
            return False
        finally:
            cursor.close()
            conn.close()

    def getMovies(self, title):

        # Setting Connection
        conn = self._connection()

        if not conn:
            print('Error connecting to database!')
            return False

        cursor = conn.cursor(dictionary=True)  # returns rows as dict instead of tuple
        query = "SELECT * FROM Movies WHERE title = %s"
        values = (title,)

        try:
            cursor.execute(query, values)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print('Error fetching movies: {}'.format(e))
            return False
        finally:
            cursor.close()
            conn.close()
