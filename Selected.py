import os
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
from Classes.MoviesCntrl_Class import MoviesCntrl


class SelectedScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, movie_data=None):
        super().__init__(parent, fg_color="#E8FFD7")
        self.controller = controller
        self.movie_data = movie_data or {}
        self.movie_ctrl = MoviesCntrl()
        self.selected_date = datetime.now().date()
        self.selected = {"seat": None, "time": None, "gate": None, "showtime_id": None}

        # ========== MAIN GRID CONFIG ==========
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=2)

        # ========== HEADER ==========
        headerFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")
        headerFrame.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        headerFrame.columnconfigure(0, weight=1)

        ctk.CTkButton(
            headerFrame,
            text="Return to Menu",
            font=("Arial", 16, "bold"),
            text_color="#3E5F44",
            fg_color="#E8FFD7",
            hover_color="#5E936C",
            corner_radius=8,
            command=lambda: controller.show_frame("HomePage")
        ).grid(row=0, column=0, sticky="w")

        # ========== MAIN CONTENT ==========
        mainFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")
        mainFrame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=2)

        # ---------- MOVIE POSTER ----------
        self.poster_frame = ctk.CTkFrame(
            mainFrame, fg_color="#E8FFD7", border_color="#3E5F44", border_width=3, corner_radius=12
        )
        self.poster_frame.grid(row=0, column=0, sticky="n", padx=15, pady=15)

        placeholder_img = Image.new("RGB", (400, 600), "#E8FFD7")
        self.img = ctk.CTkImage(light_image=placeholder_img, dark_image=placeholder_img, size=(400, 600))
        self.poster_label = ctk.CTkLabel(self.poster_frame, image=self.img, text="", fg_color="#E8FFD7")
        self.poster_label.pack(padx=10, pady=10)

        # ---------- MOVIE INFO ----------
        infoFrame = ctk.CTkFrame(mainFrame, fg_color="#E8FFD7")
        infoFrame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        infoFrame.columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            infoFrame, text="", font=("Arial", 28, "bold"), text_color="#3E5F44", anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 15))

        self.desc_label = ctk.CTkLabel(
            infoFrame, text="", font=("Arial", 12), text_color="#3E5F44", anchor="w",
            justify="left", wraplength=700
        )
        self.desc_label.grid(row=1, column=0, sticky="w", pady=(0, 20))

        # ========== TIME & GATE ==========
        timeGateSection = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")
        timeGateSection.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        timeGateSection.columnconfigure(0, weight=0)
        timeGateSection.columnconfigure(1, weight=1)

        # Time Subsection
        timeSubsection = ctk.CTkFrame(timeGateSection, fg_color="#E8FFD7")
        timeSubsection.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(
            timeSubsection, text="Available Time", font=("Arial", 14, "bold"),
            text_color="#3E5F44", anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.timeContainer = ctk.CTkFrame(timeSubsection, fg_color="#E8FFD7")
        self.timeContainer.grid(row=1, column=0, sticky="w")
        self.timeContainer.columnconfigure(tuple(range(2)), weight=1)
        self.time_buttons = []

        # Seat Subsection
        seatSubsection = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")
        seatSubsection.grid(row=3, column=0, sticky="nsew", pady=(20, 0))
        ctk.CTkLabel(
            seatSubsection, text="Available Seats", font=("Arial", 14, "bold"),
            text_color="#3E5F44", anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.seatContainer = ctk.CTkFrame(seatSubsection, fg_color="#E8FFD7")
        self.seatContainer.grid(row=1, column=0, sticky="w")
        self.seatContainer.columnconfigure(tuple(range(5)), weight=1)
        self.seat_buttons = []

        # Gate Subsection
        gateSubsection = ctk.CTkFrame(timeGateSection, fg_color="#E8FFD7")
        gateSubsection.grid(row=0, column=2, sticky="nsew", padx=(0, 80))
        ctk.CTkLabel(
            gateSubsection, text="Cinema Gate", font=("Arial", 14, "bold"),
            text_color="#3E5F44", anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        gateContainer = ctk.CTkFrame(gateSubsection, fg_color="#E8FFD7")
        gateContainer.grid(row=1, column=0, sticky="w")
        gateContainer.columnconfigure(tuple(range(2)), weight=1)
        self.gate_buttons = []

        gates = self.movie_ctrl.get_available_gates()
        for i, gate in enumerate(gates):
            row, col = divmod(i, 2)
            btn = ctk.CTkButton(
                gateContainer, text=gate["name"], font=("Arial", 12, "bold"),
                text_color="#3E5F44", fg_color="#93DA97",
                hover_color="#5E936C", corner_radius=8,
                width=120, height=40,
                command=lambda g=gate["name"]: self.select_option(g, "gate")
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.gate_buttons.append(btn)

        # Pricing
        self.price_label = ctk.CTkLabel(infoFrame, text="", font=("Arial", 18, "bold"), text_color="#3E5F44")
        self.price_label.grid(row=4, column=0, sticky="w", pady=(20, 0))

        # Purchase Button
        ctk.CTkButton(
            infoFrame,
            text="Purchase Tickets", font=("Arial", 16, "bold"),
            text_color="#E8FFD7", fg_color="#3E5F44",
            hover_color="#5E936C", corner_radius=10,
            width=250, height=50,
            command=lambda: self.open_modal(
                self.movie_data.get("title"),
                self.movie_data.get("rating"),
                self.selected.get("seat"),
                self.selected.get("time"),
                self.selected.get("gate"),
                self.selected_date.strftime("%B %d, %Y"),
                self.movie_data.get("price")
            )
        ).grid(row=5, column=0, sticky="w", pady=(20, 10))

        # ========================= MODAL BACKGROUND =========================

        # Modal Frame
        self.orderFrame = ctk.CTkFrame(self, fg_color="#E8FFD7", width=300, corner_radius=12)
        self.orderFrame.grid(row=0, column=1, rowspan=2, sticky="ns", padx=20)
        self.orderFrame.grid_propagate(False)
        self.orderFrame.bind("<Button-1>", lambda e: self.close_modal())
        self.orderFrame.grid_remove()

        # 1️⃣ Bind the main frame (self) to close the modal when clicking outside
        infoFrame.bind("<Button-1>", lambda e: self.close_modal())

        # 2️⃣ Prevent clicks inside the modal from closing it
        self.orderFrame.bind("<Button-1>", lambda e: "break")

    # ========================= DYNAMIC UPDATE =========================
    def update_selected_movie(self, movie_data):
        self.movie_data = movie_data
        self.title_label.configure(text=movie_data["title"])
        self.desc_label.configure(text=movie_data["description"])
        self.price_label.configure(text=f"Ticket Price: ₱{movie_data['price']:.2f}")

        img_path = os.path.join(os.path.dirname(__file__), "Assets", movie_data["poster"])
        try:
            img = Image.open(img_path).resize((400, 600), Image.LANCZOS)
            self.img.configure(light_image=img, dark_image=img)
        except Exception as e:
            print("Poster not found:", e)

        showtimes = self.movie_ctrl.get_available_showtimes(movie_data["id"], self.selected_date)
        self.display_showtimes(showtimes)

    # ========================= SHOWTIMES =========================
    def display_showtimes(self, showtimes):
        for btn in self.time_buttons:
            btn.destroy()
        self.time_buttons.clear()

        if not showtimes:
            ctk.CTkLabel(self.timeContainer, text="No showtimes available",
                         font=("Arial", 12), text_color="#ef4444").grid(row=0, column=0, columnspan=2, pady=10)
            return

        for i, s in enumerate(showtimes):
            btn = ctk.CTkButton(
                self.timeContainer,
                text=f"{s['start_time']} — {s['end_time']}",
                font=("Arial", 12),
                fg_color="#93DA97", text_color="#3E5F44",
                hover_color="#5E936C", width=160, height=40, corner_radius=6,
                command=lambda sid=s["showtime_id"], t=s["start_time"]: self.select_time(sid, t)
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="w")
            self.time_buttons.append(btn)

    # ========================= TIME & SEAT SELECTION =========================
    def select_time(self, showtime_id, time):
        self.selected["time"] = time
        self.selected["showtime_id"] = showtime_id
        for btn in self.time_buttons:
            btn.configure(fg_color="#3E5F44" if time in btn.cget("text") else "#93DA97",
                          text_color="#E8FFD7" if time in btn.cget("text") else "#3E5F44")

        if self.selected["gate"]:
            gate_id = self.movie_ctrl.get_gate_id_by_name(self.selected["gate"])
            self.load_seats(showtime_id, gate_id)

    def select_option(self, value, group, showtime_id=None):
        button_groups = {"time": self.time_buttons, "gate": self.gate_buttons, "seat": self.seat_buttons}
        for btn in button_groups[group]:
            btn.configure(fg_color="#93DA97", text_color="#3E5F44")
            if btn.cget("text") == value:
                btn.configure(fg_color="#3E5F44", text_color="#E8FFD7")

        self.selected[group] = value
        if showtime_id:
            self.selected["showtime_id"] = showtime_id

        if group in ("gate", "time") and self.selected["showtime_id"] and self.selected["gate"]:
            gate_id = self.movie_ctrl.get_gate_id_by_name(self.selected["gate"])
            self.load_seats(self.selected["showtime_id"], gate_id)

    # ========================= SEATS =========================
    def load_seats(self, showtime_id, gate_id):
        # Clear previous seats / labels
        for btn in self.seat_buttons:
            btn.destroy()
        self.seat_buttons.clear()

        seats = self.movie_ctrl.get_available_seats(showtime_id, gate_id)
        if not seats:
            no_seat_label = ctk.CTkLabel(
                self.seatContainer, text="No seats available",
                font=("Arial", 12), text_color="#ef4444"
            )
            no_seat_label.grid(row=0, column=0, pady=10)
            self.seat_buttons.append(no_seat_label)  # track it so it can be destroyed later
            return

        for i, seat in enumerate(seats):
            seat_label = f"{seat.get('row_label', seat.get('row', ''))}{seat.get('seat_number', seat.get('number', ''))}"
            btn = ctk.CTkButton(
                self.seatContainer, text=seat_label, font=("Arial", 12, "bold"),
                text_color="#3E5F44", fg_color="#93DA97", hover_color="#5E936C",
                corner_radius=8, width=60, height=40,
                command=lambda s=seat_label: self.select_option(s, "seat")
            )
            btn.grid(row=i // 10, column=i % 10, padx=5, pady=5)
            self.seat_buttons.append(btn)

    # ========================= MODAL =========================
    def open_modal(self, title, rating, seat, time, gate, date, price):
        if not all([seat, time, gate]):
            messagebox.showerror("Error", "Please select Time, Seat, and Gate before continuing.")
            return

        transaction_code = self.controller.transaction_code
        self.controller.transactions.setdefault(transaction_code, [])
        self.controller.transactions[transaction_code].append({
            "title": title, "rating": rating, "seat": seat, "time": time,
            "gate": gate, "date": date, "price": price
        })

        self.orderFrame.grid()
        for widget in self.orderFrame.winfo_children():
            widget.destroy()

        # Modal content
        ctk.CTkLabel(self.orderFrame, text="Order Confirmation",
                     font=("Arial", 20, "bold"), text_color="#3E5F44", anchor="nw")\
            .pack(pady=(20, 10), padx=20, anchor="w")

        for idx, ticket in enumerate(self.controller.transactions[transaction_code], start=1):
            ticket_text = (
                f"Ticket {idx}:\n🎬 {ticket['title']} ({ticket['rating']})\n"
                f"Date: {ticket['date']}\nTime: {ticket['time']}\nGate: {ticket['gate']}\n"
                f"Seat: {ticket['seat']}\nPrice: ₱{ticket['price']:.2f}"
            )
            ctk.CTkLabel(self.orderFrame, text=ticket_text,
                         font=("Arial", 14), text_color="#3E5F44",
                         anchor="w", justify="left").pack(pady=(5, 10), padx=20, anchor="w")

        total_amount = sum(t["price"] for t in self.controller.transactions[transaction_code])
        ctk.CTkLabel(self.orderFrame, text=f"Total Amount: ₱{total_amount:.2f}",
                     font=("Arial", 16, "bold"), text_color="#3E5F44", anchor="w")\
            .pack(pady=(10, 15), padx=20, anchor="w")

        ctk.CTkButton(self.orderFrame, text="Proceed to Checkout",
                      font=("Arial", 14, "bold"), text_color="#E8FFD7", fg_color="#3E5F44",
                      hover_color="#5E936C", width=150, height=40,
                      command=self.proceed_to_checkout).pack(pady=20)

    def close_modal(self):
        self.orderFrame.grid_remove()

    def proceed_to_checkout(self):
        if not self.selected["showtime_id"]:
            messagebox.showerror("Error", "Please select a showtime first.")
            return
        self.controller.show_frame("OrderCodeScreen")
