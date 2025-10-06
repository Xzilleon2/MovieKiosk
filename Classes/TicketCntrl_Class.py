from Classes.Ticket_Class import Ticket
from datetime import datetime


class TicketCntrl(Ticket):

    def __init__(self, ticket_data=None):
        super().__init__()
        # Initialize an empty dictionary if no data is passed
        self.ticket_data = ticket_data if ticket_data is not None else {}

    def insert_ticket_data(self, ticket_data, transaction_code):
        """
        Stores tickets in the internal dictionary under the transaction code.
        Multiple tickets can share the same code.
        """
        if not transaction_code:
            raise ValueError("Transaction code is required!")

        # Append new tickets under this transaction code
        self.ticket_data.setdefault(transaction_code, [])
        self.ticket_data[transaction_code].extend(ticket_data.get(transaction_code, []))

        # Validate tickets
        error = self.__checkErrors(transaction_code)
        if error:
            raise ValueError(error)

        # Flatten tickets for DB insert
        tickets_to_insert = [
            {**t, "CODE": transaction_code} for t in self.ticket_data[transaction_code]
        ]
        print(f"[DEBUG] Tickets to insert for transaction '{transaction_code}':")
        for ticket in tickets_to_insert:
            print(f"ticket content: {ticket}")
        self._insert_tickets(tickets_to_insert)

    def __checkErrors(self, transaction_code):
        """
        Ensure all required fields exist for tickets under a transaction code
        """
        if transaction_code not in self.ticket_data or not self.ticket_data[transaction_code]:
            return f"No tickets found for code {transaction_code}"

        for ticket in self.ticket_data[transaction_code]:
            required_fields = ["movie_id", "showtime_id", "seat_id", "price"]
            for field in required_fields:
                if field not in ticket or ticket[field] is None:
                    return f"Missing field '{field}' in ticket {ticket}"
        return None
