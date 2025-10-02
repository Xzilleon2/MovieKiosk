import os
import customtkinter as ctk
from PIL import Image
from Classes.MoviesCntrl_Class  import MoviesCntrl
from tkinter import messagebox
from datetime import datetime, timedelta


class SelectedScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, movie_data=None):
        super().__init__(parent, fg_color="#E8FFD7")
        self.controller = controller
        self.movie_data = movie_data or {
            "id": 4,
            "title": "Pet Sematary",
            "description": (
                "Dr. Richard, a distinguished archaeologist and professor, resides with his spouse, "
                "Dr. Jules, and their young son, Owen, on the secluded family estate inherited from "
                "Richard's late father. Owen, a child with asthma, confides in his mother..."
            ),
            "poster": "PetSematary.png",
            "price": 300.0,
            "duration": 135
        }
        self.movie_ctrl = MoviesCntrl()
        self.selected_date = datetime.now().date()  # Default to today

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=2)

        # ========== HEADER FRAME ==========
        headerFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")
        headerFrame.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        headerFrame.columnconfigure(0, weight=1)

        backButton = ctk.CTkButton(
            headerFrame,
            text="Return to Menu",
            font=("Arial", 16, "bold"),
            text_color="#3E5F44",
            fg_color="#E8FFD7",
            hover_color="#5E936C",
            corner_radius=8,
            command=lambda: controller.show_frame("HomePage")
        )
        backButton.grid(row=0, column=0, sticky="w")

        # ========== MAIN CONTENT FRAME ==========
        mainFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")
        mainFrame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=2)

        # Poster Image with Shadow
        imgpath = os.path.join(os.path.dirname(__file__), "Assets", self.movie_data["poster"])
        try:
            img = Image.open(imgpath).resize((400, 600), Image.LANCZOS)
            self.img = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 600))
        except Exception:
            self.img = ctk.CTkImage(light_image=Image.new("RGB", (400, 600), "#E8FFD7"), size=(400, 600))

        shadow_frame = ctk.CTkFrame(
            mainFrame,
            fg_color="#E8FFD7",
            border_color="#3E5F44",
            border_width=3,
            corner_radius=12
        )
        shadow_frame.grid(row=0, column=0, sticky="n", padx=15, pady=15)

        imgLabel = ctk.CTkLabel(
            shadow_frame,
            image=self.img,
            text="",
            fg_color="#E8FFD7"
        )
        imgLabel.pack(padx=10, pady=10)

        # Info Frame
        infoFrame = ctk.CTkFrame(mainFrame, fg_color="#E8FFD7")
        infoFrame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        infoFrame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            infoFrame,
            text=self.movie_data["title"],
            font=("Arial", 28, "bold"),
            text_color="#3E5F44",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        ctk.CTkLabel(
            infoFrame,
            text=self.movie_data["description"],
            font=("Arial", 12),
            text_color="#3E5F44",
            anchor="w",
            justify="left",
            wraplength=500
        ).grid(row=1, column=0, sticky="w", pady=(0, 20))

        # ========== SEATING SECTION ==========
        seatSection = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")
        seatSection.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        seatSection.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            seatSection,
            text="Available Seating",
            font=("Arial", 14, "bold"),
            text_color="#3E5F44",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        seatContainer = ctk.CTkFrame(seatSection, fg_color="#E8FFD7")
        seatContainer.grid(row=1, column=0, sticky="w")
        seatContainer.columnconfigure(tuple(range(10)), weight=1)

        self.seat_buttons = []
        seats = [f"{row}{num}" for row in ["A", "B", "C"] for num in range(1, 11)]  # A1–A10, B1–B10, C1–C10
        for i, seat in enumerate(seats):
            row = i // 10
            col = i % 10
            btn = ctk.CTkButton(
                seatContainer,
                text=seat,
                font=("Arial", 12, "bold"),
                text_color="#3E5F44",
                fg_color="#93DA97",
                hover_color="#5E936C",
                corner_radius=8,
                width=50,
                height=40,
                command=lambda s=seat: self.select_option(s, "seat")
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.seat_buttons.append(btn)

        # ========== TIME AND GATE SECTION ==========
        timeGateSection = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")
        timeGateSection.grid(row=3, column=0, sticky="nsew", pady=(20, 0))
        timeGateSection.columnconfigure(0, weight=1)
        timeGateSection.columnconfigure(1, weight=1)

        # Date Picker
        dateSubsection = ctk.CTkFrame(timeGateSection, fg_color="#E8FFD7")
        dateSubsection.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        dateSubsection.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            dateSubsection,
            text="Select Date",
            font=("Arial", 14, "bold"),
            text_color="#3E5F44",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        dateContainer = ctk.CTkFrame(dateSubsection, fg_color="#E8FFD7")
        dateContainer.grid(row=1, column=0, sticky="w")
        self.date_combobox = ctk.CTkComboBox(
            dateContainer,
            values=[datetime.now().date().strftime("%Y-%m-%d")],
            font=("Arial", 12),
            fg_color="#93DA97",
            text_color="#3E5F44",
            dropdown_fg_color="#93DA97",
            button_color="#5E936C",
            button_hover_color="#3E5F44",
            width=150,
            height=40,
            command=self.update_showtimes
        )
        self.date_combobox.grid(row=0, column=0, padx=10, pady=10)
        self.update_date_options()

        # Time Subsection
        timeSubsection = ctk.CTkFrame(timeGateSection, fg_color="#E8FFD7")
        timeSubsection.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        timeSubsection.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            timeSubsection,
            text="Showtimes",
            font=("Arial", 14, "bold"),
            text_color="#3E5F44",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.timeContainer = ctk.CTkFrame(timeSubsection, fg_color="#E8FFD7")
        self.timeContainer.grid(row=1, column=0, sticky="w")
        self.timeContainer.columnconfigure(tuple(range(2)), weight=1)
        self.time_buttons = []
        self.showtime_map = {}  # Maps time string to showtime_id
        self.update_showtimes()

        # Gate Subsection
        gateSubsection = ctk.CTkFrame(timeGateSection, fg_color="#E8FFD7")
        gateSubsection.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        gateSubsection.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            gateSubsection,
            text="Entry Gate",
            font=("Arial", 14, "bold"),
            text_color="#3E5F44",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        gateContainer = ctk.CTkFrame(gateSubsection, fg_color="#E8FFD7")
        gateContainer.grid(row=1, column=0, sticky="w")
        gateContainer.columnconfigure(tuple(range(2)), weight=1)
        self.gate_buttons = []
        gates = self.movie_ctrl.get_available_gates()
        for i, gate in enumerate(gates):
            row = i // 2
            col = i % 2
            btn = ctk.CTkButton(
                gateContainer,
                text=gate["name"],
                font=("Arial", 12, "bold"),
                text_color="#3E5F44",
                fg_color="#93DA97",
                hover_color="#5E936C",
                corner_radius=8,
                width=120,
                height=40,
                command=lambda g=gate["name"]: self.select_option(g, "gate")
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.gate_buttons.append(btn)

        # ========== PRICING SECTION ==========
        pricingFrame = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")
        pricingFrame.grid(row=4, column=0, sticky="w", pady=(20, 0))

        ctk.CTkLabel(
            pricingFrame,
            text=f"Ticket Price: ₱{self.movie_data['price']:.2f}",
            font=("Arial", 18, "bold"),
            text_color="#3E5F44"
        ).pack(anchor="w", padx=5, pady=5)

        # ========== PURCHASE BUTTON ==========
        purchaseButton = ctk.CTkButton(
            infoFrame,
            text="Purchase Tickets",
            font=("Arial", 16, "bold"),
            text_color="#E8FFD7",
            fg_color="#3E5F44",
            hover_color="#5E936C",
            corner_radius=10,
            width=250,
            height=50,
            command=self.open_modal
        )
        purchaseButton.grid(row=5, column=0, sticky="w", pady=(20, 10))

        # ========== ORDER MODAL ==========
        self.orderFrame = ctk.CTkFrame(
            self,
            fg_color="#E8FFD7",
            width=300,
            corner_radius=12,
        )
        self.orderFrame.grid(row=0, column=1, rowspan=2, sticky="ns", padx=20)
        self.orderFrame.grid_propagate(False)
        self.orderFrame.grid_remove()

        # Track selections
        self.selected = {"seat": None, "time": None, "gate": None, "showtime_id": None}

    def update_date_options(self):
        """Update date options for the next 30 days."""
        dates = []
        current_date = datetime.now().date()
        for i in range(30):
            date = current_date + timedelta(days=i)
            dates.append(date.strftime("%Y-%m-%d"))
        self.date_combobox.configure(values=dates)
        self.date_combobox.set(dates[0])

    def update_showtimes(self, *args):
        """Update showtime buttons based on selected date."""
        for widget in self.timeContainer.winfo_children():
            widget.destroy()
        self.time_buttons = []
        self.showtime_map = {}

        selected_date = datetime.strptime(self.date_combobox.get(), "%Y-%m-%d").date()
        showtimes = self.movie_ctrl.get_available_showtimes(self.movie_data["id"], selected_date)
        for i, showtime in enumerate(showtimes):
            if showtime["available_seats"] > 0:
                time_str = showtime["start_time"]
                row = i // 2
                col = i % 2
                btn = ctk.CTkButton(
                    self.timeContainer,
                    text=time_str,
                    font=("Arial", 12, "bold"),
                    text_color="#3E5F44",
                    fg_color="#93DA97",
                    hover_color="#5E936C",
                    corner_radius=8,
                    width=150,
                    height=40,
                    command=lambda t=time_str, sid=showtime["showtime_id"]: self.select_option(t, "time", sid)
                )
                btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                self.time_buttons.append(btn)
                self.showtime_map[time_str] = showtime["showtime_id"]

        if not self.time_buttons:
            ctk.CTkLabel(
                self.timeContainer,
                text="No showtimes available",
                font=("Arial", 12),
                text_color="#ef4444"
            ).grid(row=0, column=0, columnspan=2, pady=10)

    def select_option(self, value, group, showtime_id=None):
        """Handle selection of seat, time, or gate."""
        button_list = {
            "seat": self.seat_buttons,
            "time": self.time_buttons,
            "gate": self.gate_buttons
        }[group]

        for btn in button_list:
            btn.configure(fg_color="#93DA97", text_color="#3E5F44")

        for btn in button_list:
            if btn.cget("text") == value:
                btn.configure(fg_color="#3E5F44", text_color="#E8FFD7")

        self.selected[group] = value
        if group == "time":
            self.selected["showtime_id"] = showtime_id

        # Validate seat availability if time and gate are selected
        if group == "seat" and self.selected["time"] and self.selected["gate"]:
            if not self.movie_ctrl.check_seat_availability(self.selected["showtime_id"], value):
                messagebox.showerror("Error", f"Seat {value} is already booked.")
                self.selected["seat"] = None
                for btn in self.seat_buttons:
                    if btn.cget("text") == value:
                        btn.configure(fg_color="#ef4444", text_color="#E8FFD7")

    def open_modal(self):
        """Open the order confirmation modal."""
        if not all(self.selected.values()):
            messagebox.showerror("Error", "Please select a seat, showtime, and gate.")
            return

        if not self.movie_ctrl.check_seat_availability(self.selected["showtime_id"], self.selected["seat"]):
            messagebox.showerror("Error", f"Seat {self.selected['seat']} is no longer available.")
            return

        if self.orderFrame.winfo_ismapped():
            self.orderFrame.grid_remove()
            return

        self.orderFrame.grid()
        for widget in self.orderFrame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.orderFrame,
            text="Order Confirmation",
            font=("Arial", 20, "bold"),
            text_color="#3E5F44",
            anchor="nw"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        ctk.CTkLabel(
            self.orderFrame,
            text=f"Selected Options:\nSeat: {self.selected['seat']}\nShowtime: {self.selected['time']}\nEntry Gate: {self.selected['gate']}",
            font=("Arial", 14),
            text_color="#3E5F44",
            anchor="w",
            justify="left"
        ).pack(pady=(10, 15), padx=20, anchor="w")

        ctk.CTkFrame(
            self.orderFrame,
            fg_color="#93DA97",
            height=120
        ).pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            self.orderFrame,
            text=f"Total Amount: ₱{self.movie_data['price']:.2f}",
            font=("Arial", 16, "bold"),
            text_color="#3E5F44",
            anchor="w"
        ).pack(pady=(10, 15), padx=20, anchor="w")

        ctk.CTkButton(
            self.orderFrame,
            text="Proceed to Checkout",
            font=("Arial", 14, "bold"),
            text_color="#E8FFD7",
            fg_color="#3E5F44",
            hover_color="#5E936C",
            width=150,
            height=40,
            command=self.proceed_to_checkout
        ).pack(pady=20)

    def proceed_to_checkout(self):
        """Book the selected seat and proceed to checkout."""
        if self.movie_ctrl.book_seat(self.selected["showtime_id"], self.selected["seat"]):
            messagebox.showinfo("Success", "Ticket booked successfully!")
            self.controller.show_frame("OrderCodeScreen")
        else:
            messagebox.showerror("Error", "Failed to book ticket. Please try again.")