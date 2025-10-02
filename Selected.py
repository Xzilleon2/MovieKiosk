import os
import customtkinter as ctk
from PIL import Image

class SelectedScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#E8FFD7")  # Light green background
        self.controller = controller

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
            text_color="#3E5F44",  # Dark green text
            fg_color="#E8FFD7",  # Light green background
            hover_color="#5E936C",  # Hover green
            corner_radius=8,
            command=lambda: controller.show_frame("HomePage")
        )
        backButton.grid(row=0, column=0, sticky="w")

        # ========== MAIN CONTENT FRAME ==========
        mainFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")
        mainFrame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        mainFrame.columnconfigure(0, weight=1)  # Poster
        mainFrame.columnconfigure(1, weight=2)  # Info

        # Poster Image with Shadow
        imgpath = os.path.join(os.path.dirname(__file__), "Assets", "PetSematary.png")
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
            text="Pet Sematary",
            font=("Arial", 28, "bold"),
            text_color="#3E5F44",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        ctk.CTkLabel(
            infoFrame,
            text=(
                "Dr. Richard, a distinguished archaeologist and professor, resides with his spouse, "
                "Dr. Jules, and their young son, Owen, on the secluded family estate inherited from "
                "Richard's late father. Owen, a child with asthma, confides in his mother..."
            ),
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
        seats = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10",
                 "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"]
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
                command=lambda b=seat: self.select_option(b, "seat")
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.seat_buttons.append(btn)

        # ========== TIME AND GATE SECTION ==========
        timeGateSection = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")
        timeGateSection.grid(row=3, column=0, sticky="nsew", pady=(20, 0))
        timeGateSection.columnconfigure(0, weight=1)  # Time
        timeGateSection.columnconfigure(1, weight=1)  # Gate

        # Time Subsection
        timeSubsection = ctk.CTkFrame(timeGateSection, fg_color="#E8FFD7")
        timeSubsection.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        timeSubsection.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            timeSubsection,
            text="Showtimes",
            font=("Arial", 14, "bold"),
            text_color="#3E5F44",
            anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        timeContainer = ctk.CTkFrame(timeSubsection, fg_color="#E8FFD7")
        timeContainer.grid(row=1, column=0, sticky="w")
        timeContainer.columnconfigure(tuple(range(2)), weight=1)

        self.time_buttons = []
        times = ["1:00 PM - 2:00 PM", "2:00 PM - 3:00 PM", "3:00 PM - 4:00 PM", "4:00 PM - 5:00 PM"]
        for i, t in enumerate(times):
            row = i // 2
            col = i % 2
            btn = ctk.CTkButton(
                timeContainer,
                text=t,
                font=("Arial", 12, "bold"),
                text_color="#3E5F44",
                fg_color="#93DA97",
                hover_color="#5E936C",
                corner_radius=8,
                width=150,
                height=40,
                command=lambda b=t: self.select_option(b, "time")
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.time_buttons.append(btn)

        # Gate Subsection
        gateSubsection = ctk.CTkFrame(timeGateSection, fg_color="#E8FFD7")
        gateSubsection.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
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
        gates = ["Gate 1", "Gate 2", "Gate 3", "Gate 4"]
        for i, g in enumerate(gates):
            row = i // 2
            col = i % 2
            btn = ctk.CTkButton(
                gateContainer,
                text=g,
                font=("Arial", 12, "bold"),
                text_color="#3E5F44",
                fg_color="#93DA97",
                hover_color="#5E936C",
                corner_radius=8,
                width=120,
                height=40,
                command=lambda b=g: self.select_option(b, "gate")
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.gate_buttons.append(btn)

        # ========== PRICING SECTION ==========
        pricingFrame = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")
        pricingFrame.grid(row=4, column=0, sticky="w", pady=(20, 0))

        ctk.CTkLabel(
            pricingFrame,
            text="Ticket Price: ₱300.00",
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
        self.selected = {"seat": None, "time": None, "gate": None}

    def select_option(self, value, group):
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

    def open_modal(self):
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
            text="Total Amount: ₱300.00",
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
            command=lambda: self.controller.show_frame("OrderCodeScreen")
        ).pack(pady=20)