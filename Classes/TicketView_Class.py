from Classes.Ticket_Class import Ticket

class TicketView(Ticket):

    def get_tickets(self):
        """Fetch tickets from the database."""
        tickets = self._view_tickets()
        print(f"[DEBUG] Tickets fetched: {tickets}")
        return tickets

    def get_payments(self):
        """Fetch payments from the database."""
        payments = self._view_payments()
        print(f"[DEBUG] Payments fetched: {payments}")
        return payments
