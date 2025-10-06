import os
import platform
import subprocess
import glob
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
              WHERE t.status = "Booked"
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

    def _cancel_ticket(self, ticket_id):
        """
        Cancels a ticket by updating its status to 'Cancelled' in the database.
        Returns True if successful, False otherwise.
        """
        conn = self._connection()
        try:
            print(f"[DEBUG] _cancel_ticket() started for ticket_id={ticket_id}")
            query = "UPDATE tickets SET status = %s WHERE ticket_id = %s"
            values = ("Cancelled", ticket_id)

            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

            if cursor.rowcount > 0:
                print(f"[DEBUG] Ticket ID {ticket_id} successfully cancelled in DB.")
                return True
            else:
                print(f"[DEBUG] No ticket found in DB with ID {ticket_id}.")
                return False

        except Exception as e:
            print(f"[ERROR] Failed to cancel ticket {ticket_id}: {e}")
            return False

    def insert_payment(self, data):
        conn = self._connection()
        try:
            print(f"[DEBUG] insert_payment() called with: {data}")
            cursor = conn.cursor()
            sql = """
                  INSERT INTO payments (ticket_id, money, `change`, method, payment_date)
                  VALUES (%s, %s, %s, %s, %s)
                  """
            values = (
                data["ticket_id"],
                data["money"],
                data["change"],
                data.get("method", "CASH"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            cursor.execute(sql, values)
            conn.commit()
            print(f"[DEBUG] ✅ Payment inserted successfully for ticket_id={data['ticket_id']}")

            # Open latest receipt
            self.__open_latest_receipt(r"C:\xampp\htdocs\MovieKiosk\Receipts")
            return True

        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Failed to insert payment: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def __open_receipt(self, file_path):
        """Open the receipt file depending on the operating system."""
        if platform.system() == "Windows":
            os.startfile(file_path)  # Windows
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux
            subprocess.run(["xdg-open", file_path])

    def __open_latest_receipt(self, folder_path):
        list_of_files = glob.glob(f"{folder_path}\\*.txt")  # all txt files
        if not list_of_files:
            print("[ERROR] No receipt files found in folder.")
            return
        latest_file = max(list_of_files, key=os.path.getctime)  # newest file
        self.__open_receipt(latest_file)
