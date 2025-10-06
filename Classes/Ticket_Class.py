from decimal import Decimal

from Includes.Dbh import Dbh
from datetime import datetime

class Ticket(Dbh):
    def _insert_tickets(self, tickets):
        """
        tickets: list of dicts with keys:
        - CODE
        - movie_id
        - showtime_id
        - seat_id
        - price
        """
        db = self._connection()
        cursor = db.cursor()

        sql = """
            INSERT INTO tickets (CODE, movie_id, showtime_id, seat, gate, price)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = [
            (
                t["CODE"],
                t["movie_id"],
                t["showtime_id"],
                t["seat_id"],
                t["gate"],
                t["price"]
            )
            for t in tickets
        ]

        try:
            cursor.executemany(sql, values)
            db.commit()
            print(f"{cursor.rowcount} tickets inserted successfully.")
        except Exception as e:
            db.rollback()
            print("Error inserting tickets:", e)
        finally:
            cursor.close()
            db.close()

    def _view_tickets(self):
        db = self._connection()
        cursor = db.cursor(dictionary=True)

        sql = """
              SELECT t.ticket_id, \
                     t.code       AS code, \
                     m.title      AS movie_title, \
                     t.seat, \
                     s.start_time AS showtime, \
                     t.gate       AS gate, \
                     t.status, \
                     t.price
              FROM tickets t
                       JOIN movies m ON t.movie_id = m.movie_id
                       JOIN showtimes s ON t.showtime_id = s.showtime_id \
              """

        try:
            cursor.execute(sql)
            tickets = cursor.fetchall()
            print(f"{cursor.rowcount} ticket result successfully retrieved.")

            # Convert Decimal to float for price and format showtime as string
            for ticket in tickets:
                # Price: ensure float
                ticket['price'] = float(ticket['price'] or 0)

                # Gate: ensure string
                ticket['gate'] = str(ticket['gate'])

                # Showtime: format datetime if needed
                if isinstance(ticket['showtime'], datetime):
                    ticket['showtime'] = ticket['showtime'].strftime("%Y-%m-%d %H:%M:%S")

            return tickets

        except Exception as e:
            print("Error viewing tickets:", e)
            return []

        finally:
            cursor.close()
            db.close()
