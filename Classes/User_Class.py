from Includes.Dbh import Dbh

class User(Dbh):

    def _view_users(self):

        conn = self._connection()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT * FROM users
                """

        try:
         cursor.execute(query)
         user = cursor.fetchall()
         if user:
             print(f"Users data successfully fetched: {user}")
         return user
        except Exception as e:
            print(f"Failed to fetch users: {e}")
            return False