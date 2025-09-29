import mysql.connector

class Dbh:

    def _connection(self):

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='cinemakioskdb',
            )
            # Return Connection
            return conn

        except mysql.connector.Error as err:
            # Print Error Message
            print('Error connecting to MySQL database: {}'.format(err))
            return None