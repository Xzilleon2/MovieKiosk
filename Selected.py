import os
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from datetime import datetime
from Classes.MoviesCntrl_Class import MoviesCntrl


class SelectedScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, movie_data=None):
        super().__init__(parent, fg_color="#E8FFD7")
        self.controller = controller
        self.movie_data = movie_data or {}
        self.movie_ctrl = MoviesCntrl()
        self.selected_date = datetime.now().date()  # Default date
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

        # ========== TIME & GATE SECTION ==========
        timeGateSection = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")
        timeGateSection.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        timeGateSection.columnconfigure(0, weight=1)
        timeGateSection.columnconfigure(1, weight=1)

        # Date Label
        dateSubsection = ctk.CTkFrame(timeGateSection, fg_color="#E8FFD7")
        dateSubsection.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(
            dateSubsection, text="Date", font=("Arial", 14, "bold"),
            text_color="#3E5F44", anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.date_label = ctk.CTkLabel(
            dateSubsection,
            text=self.selected_date.strftime("%B %d, %Y"),
            font=("Arial", 12, "bold"),
            text_color="#3E5F44",
            fg_color="#93DA97",
            width=150, height=40, corner_radius=6
        )
        self.date_label.grid(row=1, column=0, padx=10, pady=10)

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

        # ========== SEATS SECTION ==========
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

        # ========== GATE SECTION ==========
        gateSubsection = ctk.CTkFrame(timeGateSection, fg_color="#E8FFD7")
        gateSubsection.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
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

        # ========== PRICE SECTION ==========
        self.pricingFrame = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")
        self.pricingFrame.grid(row=4, column=0, sticky="w", pady=(20, 0))
        self.price_label = ctk.CTkLabel(
            self.pricingFrame, text="", font=("Arial", 18, "bold"), text_color="#3E5F44"
        )
        self.price_label.pack(anchor="w", padx=5, pady=5)

        # ========== PURCHASE BUTTON ==========
        ctk.CTkButton(
            infoFrame,
            text="Purchase Tickets", font=("Arial", 16, "bold"),
            text_color="#E8FFD7", fg_color="#3E5F44",
            hover_color="#5E936C", corner_radius=10,
            width=250, height=50, command=self.open_modal
        ).grid(row=5, column=0, sticky="w", pady=(20, 10))

        # ========== ORDER MODAL ==========
        self.orderFrame = ctk.CTkFrame(self, fg_color="#E8FFD7", width=300, corner_radius=12)
        self.orderFrame.grid(row=0, column=1, rowspan=2, sticky="ns", padx=20)
        self.orderFrame.grid_propagate(False)
        self.orderFrame.grid_remove()

    # =========================================================
    # ✅ DYNAMIC UPDATE
    # =========================================================
    def update_selected_movie(self, movie_data):
        """Update movie details dynamically."""
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

    # =========================================================
    # ✅ Populate Showtimes from DB (with seat count)
    # =========================================================
    def display_showtimes(self, showtimes):
        """Display showtimes dynamically."""
        for btn in self.time_buttons:
            btn.destroy()
        self.time_buttons.clear()

        if not showtimes:
            ctk.CTkLabel(
                self.timeContainer, text="No showtimes available",
                font=("Arial", 12), text_color="#ef4444"
            ).grid(row=0, column=0, columnspan=2, pady=10)
            return

        for i, s in enumerate(showtimes):
            time_text = f"{s['start_time']}  —  {s['available_seats']} seats"
            btn = ctk.CTkButton(
                self.timeContainer,
                text=time_text, font=("Arial", 12),
                fg_color="#93DA97", text_color="#3E5F44",
                hover_color="#5E936C", width=160, height=40,
                corner_radius=6,
                command=lambda sid=s["showtime_id"], t=s["start_time"]: self.select_time(sid, t)
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="w")
            self.time_buttons.append(btn)

    def select_time(self, showtime_id, time):
        """Handles time selection (does not load seats yet)."""
        self.selected["time"] = time
        self.selected["showtime_id"] = showtime_id

        # Highlight selected time
        for btn in self.time_buttons:
            if time in btn.cget("text"):
                btn.configure(fg_color="#3E5F44", text_color="#E8FFD7")
            else:
                btn.configure(fg_color="#93DA97", text_color="#3E5F44")

        # ✅ Only trigger seat loading when both gate and time are selected
        if self.selected["gate"]:
            gate_id = self.movie_ctrl.get_gate_id_by_name(self.selected["gate"])
            print(f"[DEBUG] Time selected → {time}, Showtime ID: {showtime_id}, Gate: {self.selected['gate']}")
            self.load_seats(showtime_id, gate_id)
        else:
            print(f"[DEBUG] Time selected ({time}), waiting for gate selection.")

    # =========================================================
    # ✅ Load Available Seats when Showtime Selected
    # =========================================================
    def load_seats(self, showtime_id, gate_id):
        print(f"[UI] load_seats() triggered with showtime_id={showtime_id}")
        self.selected["showtime_id"] = showtime_id
        self.selected["gate_id"] = gate_id

        for btn in self.seat_buttons:
            btn.destroy()
        self.seat_buttons.clear()

        seats = self.movie_ctrl.get_available_seats(showtime_id, gate_id)
        print(f"[UI] Retrieved {len(seats)} seats from controller")

        if not seats:
            print("[UI] No seats received — model likely returned empty list.")
            ctk.CTkLabel(
                self.seatContainer, text="No seats available", font=("Arial", 12), text_color="#ef4444"
            ).grid(row=0, column=0, pady=10)
            return

        # ✅ Render seat buttons dynamically
        for i, seat in enumerate(seats):
            try:
                seat_label = f"{seat['row_label']}{seat['seat_number']}"
            except KeyError:
                # fallback if your DB uses different column names
                seat_label = f"{seat.get('row', '')}{seat.get('number', '')}"

            btn = ctk.CTkButton(
                self.seatContainer,
                text=seat_label,
                font=("Arial", 12, "bold"),
                text_color="#3E5F44",
                fg_color="#93DA97",
                hover_color="#5E936C",
                corner_radius=8,
                width=60, height=40,
                command=lambda s=seat_label: self.select_option(s, "seat")
            )
            btn.grid(row=i // 10, column=i % 10, padx=5, pady=5)
            self.seat_buttons.append(btn)

        print(f"[UI] Rendered {len(self.seat_buttons)} seat buttons successfully.")

    # =========================================================
    # ✅ Selection Logic
    # =========================================================
    def select_option(self, value, group, showtime_id=None):
        """Handles selection of gate, time, and seat groups."""
        button_groups = {
            "time": self.time_buttons,
            "gate": self.gate_buttons,
            "seat": self.seat_buttons
        }

        # Reset colors for this group
        for btn in button_groups[group]:
            btn.configure(fg_color="#93DA97", text_color="#3E5F44")

        # Highlight selected button
        for btn in button_groups[group]:
            if btn.cget("text").startswith(value):
                btn.configure(fg_color="#3E5F44", text_color="#E8FFD7")

        # Store the selection
        self.selected[group] = value
        if showtime_id:
            self.selected["showtime_id"] = showtime_id

        # ✅ If both time and gate are selected, load seats
        if self.selected["showtime_id"] and self.selected["gate"]:
            gate_id = self.movie_ctrl.get_gate_id_by_name(self.selected["gate"])
            print(f"[DEBUG] Gate selected → {value}, Gate ID: {gate_id}")
            print(f"[DEBUG] Showtime selected → {self.selected['showtime_id']}")
            self.load_seats(self.selected["showtime_id"], gate_id)
        else:
            print(f"[DEBUG] {group.capitalize()} selected ({value}), waiting for other selection.")

    # =========================================================
    # ✅ Purchase Modal Logic
    # =========================================================
    def open_modal(self):
        if not all([self.selected["showtime_id"], self.selected["seat"], self.selected["gate"]]):
            messagebox.showerror("Error", "Please select Time, Seat, and Gate before continuing.")
            return

        if self.orderFrame.winfo_ismapped():
            self.orderFrame.grid_remove()
            return

        self.orderFrame.grid()
        for widget in self.orderFrame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.orderFrame, text="Order Confirmation", font=("Arial", 20, "bold"),
            text_color="#3E5F44", anchor="nw"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        ctk.CTkLabel(
            self.orderFrame,
            text=f"Selected:\nTime: {self.selected['time']}\nGate: {self.selected['gate']}\nSeat: {self.selected['seat']}",
            font=("Arial", 14),
            text_color="#3E5F44", anchor="w", justify="left"
        ).pack(pady=(10, 15), padx=20, anchor="w")

        ctk.CTkLabel(
            self.orderFrame,
            text=f"Total Amount: ₱{self.movie_data['price']:.2f}",
            font=("Arial", 16, "bold"), text_color="#3E5F44", anchor="w"
        ).pack(pady=(10, 15), padx=20, anchor="w")

        ctk.CTkButton(
            self.orderFrame,
            text="Proceed to Checkout", font=("Arial", 14, "bold"),
            text_color="#E8FFD7", fg_color="#3E5F44",
            hover_color="#5E936C", width=150, height=40,
            command=self.proceed_to_checkout
        ).pack(pady=20)

    def proceed_to_checkout(self):
        if not self.selected["showtime_id"]:
            messagebox.showerror("Error", "Please select a showtime first.")
            return
        self.controller.show_frame("OrderCodeScreen")
