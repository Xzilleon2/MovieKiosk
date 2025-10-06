import customtkinter as ctk
from Modals.Delete import delete_modal
from Modals.Update import update_modal
from Classes.TicketView_Class import TicketView
from datetime import datetime


class SalesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#E8FFD7")

        # Main layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=1)

        # ================= Sidebar ================= #
        sidebar = ctk.CTkFrame(self, fg_color="#93DA97", corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)

        logoLabel = ctk.CTkLabel(sidebar, text="🎬 Admin",
                                 font=("Book Antiqua", 18, "bold"),
                                 text_color="#3E5F44")
        logoLabel.grid(row=0, column=0, sticky="nsew", pady=(30, 40))

        def menu_button(text, row, active=False, command=None):
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Book Antiqua", 13),
                fg_color="#5E936C" if active else "#93DA97",
                text_color="#3E5F44",
                hover_color="#E8FFD7",
                corner_radius=6,
                command=command
            )
            btn.grid(row=row, column=0, sticky="ew", padx=15, pady=3, ipady=10)
            return btn

        menu_button("Movies", 2, command=lambda: controller.show_frame("AdminPage"))
        menu_button("Sales", 3, active=True, command=lambda: controller.show_frame("SalesPage"))
        menu_button("Sales History", 4, command=lambda: controller.show_frame("SalesHistoryPage"))

        logoutBtn = ctk.CTkButton(sidebar, text="Logout",
                                  font=("Book Antiqua", 12),
                                  fg_color="#3E5F44", text_color="#E8FFD7",
                                  hover_color="#5E936C", corner_radius=6)
        logoutBtn.grid(row=6, column=0, sticky="sew", padx=15, pady=(10, 20), ipady=8)

        # ================= Main Content ================= #
        mainFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")
        mainFrame.grid(row=0, column=1, sticky="nsew")
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)  # Table row grows

        # ---- Title ---- #
        title = ctk.CTkLabel(mainFrame, text="Sales Management",
                             font=("Book Antiqua", 18, "bold"),
                             text_color="#3E5F44")
        title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # ---- Table card ---- #
        tableCard = ctk.CTkFrame(mainFrame, fg_color="#93DA97", corner_radius=12)
        tableCard.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        tableCard.columnconfigure(tuple(range(7)), weight=1)

        # Top bar inside table card
        cardTop = ctk.CTkFrame(tableCard, fg_color="#93DA97")
        cardTop.grid(row=0, column=0, columnspan=7, sticky="ew", padx=10, pady=(30, 5))
        cardTop.columnconfigure(0, weight=1)
        cardTop.columnconfigure(1, weight=0)

        self.search_entry = ctk.CTkEntry(cardTop, placeholder_text="Search...",
                                         font=("Book Antiqua", 12), width=250,
                                         height=30, fg_color="#E8FFD7", text_color="#3E5F44")
        self.search_entry.grid(row=0, column=1, sticky="e", padx=10)
        self.search_entry.bind("<KeyRelease>", self.handle_search)  # Bind search event

        # Table headers
        headers = ["ID", "Code", "Movie Title", "Seat", "Showtime", "Gate", "Price", "Action"]
        self.headers = headers
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(tableCard,
                               text=h,
                               font=("Book Antiqua", 13, "bold"),
                               text_color="#3E5F44", fg_color="#E8FFD7",
                               corner_radius=6, pady=8)
            lbl.grid(row=1, column=i, sticky="nsew", padx=5, pady=10)

        # Pagination setup
        self.page_size = 10
        self.current_page = 0
        self.tableCard = tableCard
        self.all_tickets = TicketView().get_tickets() or []
        self.filtered_tickets = self.all_tickets
        self.render_page()

        # ---- Pagination controls ---- #
        pagination = ctk.CTkFrame(mainFrame, fg_color="#E8FFD7")
        pagination.grid(row=2, column=0, sticky="ew", pady=(0, 60))

        prevBtn = ctk.CTkButton(
            pagination,
            text="◀ Previous",
            fg_color="#93DA97",
            text_color="#3E5F44",
            hover_color="#5E936C",
            corner_radius=6,
            width=100,
            command=self.prev_page
        )
        prevBtn.pack(side="left", padx=20)

        nextBtn = ctk.CTkButton(
            pagination,
            text="Next ▶",
            fg_color="#93DA97",
            text_color="#3E5F44",
            hover_color="#5E936C",
            corner_radius=6,
            width=100,
            command=self.next_page
        )
        nextBtn.pack(side="right", padx=20)

    # ================= Helper Methods ================= #
    def handle_search(self, event=None):
        """Handle search input and filter tickets."""
        query = self.search_entry.get().strip().lower()
        if query:
            # Filter tickets based on movie_title
            self.filtered_tickets = [
                ticket for ticket in self.all_tickets
                if query in ticket["movie_title"].lower()
            ]
        else:
            # If search is empty, show all tickets
            self.filtered_tickets = self.all_tickets

        self.current_page = 0  # Reset to first page on search
        self.render_page()

    def render_page(self):
        """Render the current page of tickets (filtered or all)."""
        # Clear old rows
        for widget in self.tableCard.winfo_children()[len(self.headers) + 1:]:
            widget.destroy()

        # Use filtered tickets if available, else use all tickets
        self.rows = self.filtered_tickets if self.filtered_tickets else None

        # Display message if no tickets are found
        if not self.rows:
            lbl = ctk.CTkLabel(self.tableCard, text="No tickets found",
                               font=("Book Antiqua", 12), text_color="#3E5F44")
            lbl.grid(row=2, column=0, columnspan=len(self.headers), pady=20)
            return

        start = self.current_page * self.page_size
        end = start + self.page_size

        for r, ticket in enumerate(self.rows[start:end], start=2):
            for c, header in enumerate(self.headers):
                if header == "Price":
                    price_text = f"₱{ticket['price']:.2f}" if isinstance(ticket['price'], (int, float)) else "Invalid Price"
                    lbl = ctk.CTkLabel(self.tableCard, text=price_text,
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Showtime":
                    try:
                        # Format showtime (e.g., "2025-10-05 10:00:00" to "Oct 05, 2025 10:00 AM")
                        showtime = datetime.strptime(ticket["showtime"], "%Y-%m-%d %H:%M:%S")
                        showtime_text = showtime.strftime("%b %d, %Y %I:%M %p")
                    except (ValueError, TypeError):
                        showtime_text = ticket["showtime"] if ticket["showtime"] else "Invalid Showtime"
                    lbl = ctk.CTkLabel(self.tableCard, text=showtime_text,
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Action":
                    action_frame = ctk.CTkFrame(self.tableCard, fg_color="#93DA97")
                    action_frame.grid(row=r, column=c, sticky="nsew", padx=5, pady=8)
                    action_frame.columnconfigure((0, 1), weight=1)

                    # Delete Button
                    del_btn = ctk.CTkButton(
                        action_frame, text="⛔", width=30, height=30, font=("Book Antiqua", 12),
                        fg_color="#ef4444", hover_color="#dc2626",
                        command=lambda t_id=ticket["ticket_id"], m_title=ticket["movie_title"]: delete_modal(self, t_id, m_title)
                    )
                    del_btn.grid(row=0, column=0, padx=2, sticky="nsew")

                    # Update Button
                    upd_btn = ctk.CTkButton(
                        action_frame, text="💵", width=30, height=30, font=("Book Antiqua", 12),
                        fg_color="#22c55e", hover_color="#16a34a",
                        command=lambda t_id=ticket["ticket_id"], m_title=ticket["movie_title"],
                                      t_seat=ticket["seat"], t_showtime=ticket["showtime"], t_price=ticket["price"]:
                        update_modal(self, t_id, m_title, t_seat, t_showtime, t_price)
                    )
                    upd_btn.grid(row=0, column=1, padx=2, sticky="nsew")

                else:
                    # Default mapping: ID, Movie Title, Seat, Gate
                    key = header.lower().replace(" ", "_")
                    if header == "ID":
                        key = "ticket_id"
                    elif key == "movie_title":
                        key = "movie_title"
                    lbl = ctk.CTkLabel(self.tableCard, text=ticket.get(key, ""),
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

    def next_page(self):
        """Go to the next page of tickets."""
        if (self.current_page + 1) * self.page_size < len(self.rows):
            self.current_page += 1
            self.render_page()

    def prev_page(self):
        """Go to the previous page of tickets."""
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page()

    def refresh_tickets(self):
        """Refresh ticket data from TicketView."""
        try:
            self.all_tickets = TicketView().get_tickets() or []
            self.filtered_tickets = self.all_tickets
            self.current_page = 0
            self.render_page()
        except Exception as e:
            lbl = ctk.CTkLabel(self.tableCard, text=f"Error loading tickets: {str(e)}",
                               font=("Book Antiqua", 12), text_color="#ef4444")
            lbl.grid(row=2, column=0, columnspan=len(self.headers), pady=20)