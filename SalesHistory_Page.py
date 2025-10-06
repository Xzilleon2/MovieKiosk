import customtkinter as ctk
from Classes.TicketView_Class import TicketView

class SalesHistoryPage(ctk.CTkFrame):
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
        menu_button("Sales", 3, command=lambda: controller.show_frame("SalesPage"))
        menu_button("Sales History", 4, active=True, command=lambda: controller.show_frame("SalesHistoryPage"))

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
        title = ctk.CTkLabel(mainFrame, text="Sales History",
                             font=("Book Antiqua", 18, "bold"),
                             text_color="#3E5F44")
        title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # ---- Table card ---- #
        tableCard = ctk.CTkFrame(mainFrame, fg_color="#93DA97", corner_radius=12)
        tableCard.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        tableCard.columnconfigure(tuple(range(7)), weight=1)

        # Top bar inside table card
        cardTop = ctk.CTkFrame(tableCard, fg_color="#93DA97")
        cardTop.grid(row=0, column=0, columnspan=10, sticky="ew", padx=10, pady=(30, 5))
        cardTop.columnconfigure(0, weight=1)
        cardTop.columnconfigure(1, weight=0)

        self.search_entry = ctk.CTkEntry(cardTop, placeholder_text="Search...",
                                         font=("Book Antiqua", 12), width=250,
                                         height=30, fg_color="#E8FFD7", text_color="#3E5F44")
        self.search_entry.grid(row=0, column=1, sticky="e", padx=10)
        self.search_entry.bind("<KeyRelease>", self.handle_search)

        # Table headers
        # Table headers
        headers = ["ID", "Code", "Seat", "Gate", "Date", "Time", "Total Payment"]
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
        self.all_payments = TicketView().get_payments()  # fetch payments
        self.filtered_payments = self.all_payments
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
        """Handle search input and filter payments."""
        query = self.search_entry.get().strip().lower()
        if query:
            self.filtered_payments = [
                p for p in self.all_payments
                if query in str(p["ticket_id"]).lower() or query in str(p["seat"]).lower()
            ]
        else:
            self.filtered_payments = self.all_payments
        self.current_page = 0
        self.render_page()

    def render_page(self):
        """Render the current page of payments."""
        for widget in self.tableCard.winfo_children()[len(self.headers) + 1:]:
            widget.destroy()

        self.rows = self.filtered_payments if self.filtered_payments else None

        if not self.rows:
            lbl = ctk.CTkLabel(self.tableCard, text="No payments found",
                               font=("Book Antiqua", 12), text_color="#3E5F44")
            lbl.grid(row=2, column=0, columnspan=len(self.headers), pady=20)
            return

        start = self.current_page * self.page_size
        end = start + self.page_size

        for r, payment in enumerate(self.rows[start:end], start=2):
            for c, header in enumerate(self.headers):
                if header == "Total Payment":
                    lbl = ctk.CTkLabel(
                        self.tableCard,
                        text=f"₱{float(payment['total_payment']):.2f}",
                        font=("Book Antiqua", 12), text_color="#3E5F44"
                    )
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Date":
                    date_text = payment["payment_date"].strftime("%Y-%m-%d")
                    lbl = ctk.CTkLabel(self.tableCard, text=date_text,
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Time":
                    time_text = payment["payment_date"].strftime("%H:%M:%S")
                    lbl = ctk.CTkLabel(self.tableCard, text=time_text,
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                else:
                    # Map header to dict key
                    key_map = {
                        "ID": "payment_id",
                        "Code": "code",
                        "Seat": "seat",
                        "Gate": "gate"
                    }
                    key = key_map.get(header, header.lower().replace(" ", "_"))
                    lbl = ctk.CTkLabel(self.tableCard, text=payment.get(key, ""),
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.rows):
            self.current_page += 1
            self.render_page()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page()

    def refresh_payments(self):
        try:
            self.all_payments = TicketView().get_payments() or []
            self.filtered_payments = self.all_payments
            self.current_page = 0
            self.render_page()
        except Exception as e:
            lbl = ctk.CTkLabel(self.tableCard, text=f"Error loading payments: {str(e)}",
                               font=("Book Antiqua", 12), text_color="#ef4444")
            lbl.grid(row=2, column=0, columnspan=len(self.headers), pady=20)
