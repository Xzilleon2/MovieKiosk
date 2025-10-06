import customtkinter as ctk
from Includes.Receipt import ReceiptGenerator
from Modals.Cancel import cancel_modal
from Classes.TicketView_Class import TicketView
from Classes.TicketCntrl_Class import TicketCntrl
from datetime import datetime
import tkinter.messagebox as messagebox
import os, platform, subprocess


class SalesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#E8FFD7")
        self.controller = controller  # Store controller for frame switching

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
        headers = ["ID", "Code", "Movie Title", "Seat", "Showtime", "Status", "Price", "Action"]
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

    def tkraise(self, *args, **kwargs):
        """Override tkraise to refresh tickets when frame is shown."""
        super().tkraise(*args, **kwargs)
        self.refresh_tickets()

    # ================= Helper Methods ================= #
    def status_badge(self, parent, text):
        color_map = {
            "Active": "#22c55e",
            "Inactive": "#ef4444",
            "Pending": "#f59e0b",
            "Booked": "#22c55e"
        }
        return ctk.CTkLabel(
            parent,
            text=text,
            font=("Book Antiqua", 13, "bold"),
            text_color="#E8FFD7",
            fg_color=color_map.get(text, "#6b7280"),
            corner_radius=8,
            padx=10,
            pady=4
        )

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
                        # Format showtime (e.g., "2025-10-06 14:00:00" to "Oct 06, 2025 02:00 PM")
                        showtime = datetime.strptime(ticket["showtime"], "%Y-%m-%d %H:%M:%S")
                        showtime_text = showtime.strftime("%b %d, %Y %I:%M %p")
                    except (ValueError, TypeError):
                        showtime_text = ticket.get("showtime", "Invalid Showtime")
                    lbl = ctk.CTkLabel(self.tableCard, text=showtime_text,
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Status":
                    badge = self.status_badge(self.tableCard, ticket["status"])
                    badge.grid(row=r, column=c, sticky="nsew", padx=10, pady=8)

                elif header == "Action":
                    action_frame = ctk.CTkFrame(self.tableCard, fg_color="#93DA97")
                    action_frame.grid(row=r, column=c, sticky="nsew", padx=5, pady=8)
                    action_frame.columnconfigure((0, 1), weight=1)

                    # Delete Button
                    del_btn = ctk.CTkButton(
                        action_frame, text="⛔", width=30, height=30, font=("Book Antiqua", 12),
                        fg_color="#ef4444", hover_color="#dc2626",
                        command=lambda t_id=ticket["ticket_id"], code=ticket["code"]: cancel_modal(self, t_id, code)
                    )
                    del_btn.grid(row=0, column=0, padx=2, sticky="nsew")

                    # Update Button
                    upd_btn = ctk.CTkButton(
                        action_frame, text="💵", width=30, height=30, font=("Book Antiqua", 12),
                        fg_color="#22c55e", hover_color="#16a34a",
                        command=lambda t=ticket: self.open_choice_modal(t)
                    )
                    upd_btn.grid(row=0, column=1, padx=2, sticky="nsew")

                else:
                    # Default mapping: ID, Code, Movie Title, Seat
                    key = header.lower().replace(" ", "_")
                    if header == "ID":
                        key = "ticket_id"
                    elif key == "movie_title":
                        key = "movie_title"
                    lbl = ctk.CTkLabel(self.tableCard, text=ticket.get(key, ""),
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

    def open_choice_modal(self, ticket):
        """Open choice modal with the selected ticket data."""
        from Modals.choice import choice_modal
        print(f"[DEBUG] Opening choice modal for ticket: {ticket}")

        # Store the selected ticket globally in the class
        self.current_ticket = ticket

        # Callback when Cash is chosen
        def handle_cash_payment(ticket_data):
            from Modals.Payment import payment_modal
            print(f"[DEBUG] Cash option selected. Passing ticket to payment modal: {ticket_data}")
            payment_modal(self, ticket_data, pay_callback=self.process_payment)

        # Call the choice modal and pass ticket to it
        choice_modal(self, cash_callback=handle_cash_payment, ticket=ticket)

    def process_payment(self, payment_data):
        print(f"[DEBUG] Payment confirmed. Amount entered: ₱{payment_data}")

        if not hasattr(self, "current_ticket") or not self.current_ticket:
            print("[ERROR] No ticket selected for payment.")
            return

        ticket = self.current_ticket
        total_price = ticket["price"]

        # Safely extract from payment_data dict
        money = float(payment_data.get("money", 0))
        change = float(payment_data.get("change", 0))
        method = payment_data.get("method", "Cash")

        # Prepare full payment data for controller
        full_payment = {
            "ticket_id": ticket["ticket_id"],
            "money": money,
            "change": change,
            "method": method,
            "payment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        print(f"[DEBUG] Sending payment_data to controller: {full_payment}")

        # Pass data to controller for DB insert
        controller = TicketCntrl()
        result = controller.handle_payment(full_payment, ticket)

        # === If successful, generate and open receipt automatically === #
        if result and result.get("success"):
            print("✅ Payment saved successfully, generating receipt...")

            # Prepare receipt data
            receipt_data = {
                "movie_title": ticket["movie_title"],
                "show_date": ticket.get("show_date", datetime.now().strftime("%B %d, %Y")),
                "show_time": ticket.get("showtime", ""),
                "cinema": ticket.get("gate", "Cinema 1"),
                "seat": ticket.get("seat", "N/A"),
                "ticket_code": ticket.get("code", "0001"),
                "amount": f"₱{total_price:.2f}",
                "customer_cash": f"₱{money:.2f}",
                "change": f"₱{change:.2f}",
            }

            try:
                generator = ReceiptGenerator()
                pdf_path = generator.create_receipt(receipt_data)
                print(f"✅ Receipt generated successfully at: {pdf_path}")

                # Automatically open the receipt file
                if platform.system() == "Windows":
                    os.startfile(pdf_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", pdf_path])
                else:  # Linux or others
                    subprocess.run(["xdg-open", pdf_path])

                # Refresh ticket table after successful payment
                self.refresh_tickets()

            except Exception as e:
                print(f"[ERROR] Failed to generate or open receipt: {e}")

        else:
            print(f"[ERROR] Payment failed: {result.get('message') if result else 'No result returned'}")

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