from Classes.Ticket_Class import Ticket

class TicketView(Ticket):

    def get_tickets(self):

         # Get Tickets From DB
         tickets = self._view_tickets()
         print(f"[DEBUG] Tickets fetched: {tickets}")
         return tickets