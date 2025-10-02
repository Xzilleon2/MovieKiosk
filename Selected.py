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

        # ========== UPPER FRAME ==========
        upperFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")  # Light green background
        upperFrame.grid(row=0, column=0, sticky="nsew")
        upperFrame.columnconfigure(0, weight=1)

        backButton = ctk.CTkButton(
            upperFrame,
            text="← BACK TO MENU",
            font=("Book Antiqua", 20),
            text_color="#3E5F44",  # Dark green text
            fg_color="#E8FFD7",  # Light green background
            hover_color="#5E936C",  # Hover green
            corner_radius=0,
            command=lambda: controller.show_frame("HomePage")
        )
        backButton.grid(row=0, column=0, sticky="sw", padx=15, pady=30)

        # ========== MAIN FRAME ==========
        mainFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")  # Light green background
        mainFrame.grid(row=1, column=0, sticky="nsew", padx=(20, 0))
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=2)

        # Poster Image with Shadow
        imgpath = os.path.join(os.path.dirname(__file__), "Assets", "PetSematary.png")
        img = Image.open(imgpath).resize((400, 600), Image.LANCZOS)
        self.img = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 600))

        # Create shadow frame for poster
        shadow_frame = ctk.CTkFrame(
            mainFrame,
            fg_color="#E8FFD7",  # Match background
            border_color="#3E5F44",  # Dark green for shadow
            border_width=2,
            corner_radius=8
        )
        shadow_frame.grid(row=0, column=0, sticky="n", padx=(12, 10), pady=(12, 10))

        imgLabel = ctk.CTkLabel(
            shadow_frame,
            image=self.img,
            text="",
            fg_color="#E8FFD7"  # Light green to match background
        )
        imgLabel.pack(padx=4, pady=4)  # Padding inside shadow frame

        # Info Frame
        infoFrame = ctk.CTkFrame(mainFrame, fg_color="#E8FFD7")  # Light green background
        infoFrame.grid(row=0, column=1, sticky="nsew", padx=10)
        infoFrame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            infoFrame,
            text="Pet Sematary",
            font=("Book Antiqua", 40),
            text_color="#3E5F44",  # Dark green text
            anchor="w"
        ).grid(row=0, column=0, sticky="new")

        ctk.CTkLabel(
            infoFrame,
            text=(
                "Richard, an archaeologist and professor, and his wife, Jules, "
                "live with their young son Owen on Richard's deceased father's isolated farm on the moors. "
                "Owen, an asthmatic child, tells his mother...."
            ),
            font=("Book Antiqua", 12),
            text_color="#3E5F44",  # Dark green text
            anchor="nw",
            justify="left",
            wraplength=500
        ).grid(row=1, column=0, sticky="new")

        # ========== SEATS ==========
        seatFrame = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")  # Light green background
        seatFrame.grid(row=2, column=0, sticky="nsew", pady=(20, 0))

        ctk.CTkLabel(
            seatFrame,
            text="AVAILABLE SEATS",
            font=("Book Antiqua", 12),
            text_color="#3E5F44",  # Dark green text
            anchor="w"
        ).pack(anchor="w", padx=(0, 30))

        seatFrameCon = ctk.CTkFrame(seatFrame, fg_color="#E8FFD7")  # Light green background
        seatFrameCon.pack(anchor="w")

        self.seat_buttons = []
        max_per_row = 10  # Number of seats

        for i, seat in enumerate([
            "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10",
            "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10",
        ]):
            row = i // max_per_row
            col = i % max_per_row

            btn = ctk.CTkButton(
                seatFrameCon,
                text=seat,
                font=("Book Antiqua", 14),
                text_color="#3E5F44",  # Dark green text
                fg_color="#93DA97",  # Secondary green background
                hover_color="#5E936C",  # Hover green
                corner_radius=5,
                width=60,
                command=lambda b=seat: self.select_option(b, "seat")
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            self.seat_buttons.append(btn)

        # ========== TIME ==========
        timeFrame = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")  # Light green background
        timeFrame.grid(row=3, column=0, sticky="nsew", pady=(20, 0))

        ctk.CTkLabel(
            timeFrame,
            text="TIME",
            font=("Book Antiqua", 12),
            text_color="#3E5F44",  # Dark green text
            anchor="w"
        ).pack(anchor="w", padx=(0, 30))

        timeFrameCon = ctk.CTkFrame(timeFrame, fg_color="#E8FFD7")  # Light green background
        timeFrameCon.pack(anchor="w")

        self.time_buttons = []
        max_per_row = 2

        for i, t in enumerate(["1:00 - 2:00", "2:00 - 3:00", "3:00 - 4:00", "4:00 - 5:00"]):
            row = i // max_per_row
            col = i % max_per_row

            btn = ctk.CTkButton(
                timeFrameCon,
                text=t,
                font=("Book Antiqua", 14),
                text_color="#3E5F44",  # Dark green text
                fg_color="#93DA97",  # Secondary green background
                hover_color="#5E936C",  # Hover green
                corner_radius=5,
                width=120,
                command=lambda b=t: self.select_option(b, "time")
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            self.time_buttons.append(btn)

        # ========== GATE ==========
        gateFrame = ctk.CTkFrame(infoFrame, fg_color="#E8FFD7")  # Light green background
        gateFrame.grid(row=4, column=0, sticky="nsew", pady=(20, 0))

        ctk.CTkLabel(
            gateFrame,
            text="GATE",
            font=("Book Antiqua", 12),
            text_color="#3E5F44",  # Dark green text
            anchor="w"
        ).pack(anchor="w", padx=(0, 30))

        gateFrameCon = ctk.CTkFrame(gateFrame, fg_color="#E8FFD7")  # Light green background
        gateFrameCon.pack(anchor="w")

        self.gate_buttons = []
        max_per_row = 2  # Number of gates per row

        for i, g in enumerate(["Gate 1", "Gate 2", "Gate 3", "Gate 4"]):
            row = i // max_per_row
            col = i % max_per_row

            btn = ctk.CTkButton(
                gateFrameCon,
                text=g,
                font=("Book Antiqua", 14),
                text_color="#3E5F44",  # Dark green text
                fg_color="#93DA97",  # Secondary green background
                hover_color="#5E936C",  # Hover green
                corner_radius=5,
                width=100,
                command=lambda b=g: self.select_option(b, "gate")
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="w")
            self.gate_buttons.append(btn)

        # ========== PRICE ==========
        ctk.CTkLabel(
            infoFrame,
            text="₱300.00",  # Updated to peso symbol
            font=("Book Antiqua", 30),
            text_color="#3E5F44"  # Dark green text
        ).grid(row=5, column=0, sticky="w", pady=20)

        # ========== PURCHASE BUTTON ==========
        ctk.CTkButton(
            infoFrame,
            text="Place Order",
            font=("Book Antiqua", 14),
            text_color="#E8FFD7",  # Light green text
            fg_color="#3E5F44",  # Dark green button
            hover_color="#5E936C",  # Hover green
            corner_radius=8,
            width=200,
            height=50,
            command=self.open_modal
        ).grid(row=6, column=0, sticky="w", pady=10)

        # ========== ORDER MODAL ==========
        self.orderFrame = ctk.CTkFrame(
            self,
            fg_color="#E8FFD7",  # Light green background
            width=250,
            corner_radius=10,
        )
        self.orderFrame.grid(row=0, column=1, rowspan=2, sticky="ns", padx=5)
        self.orderFrame.grid_propagate(False)
        self.orderFrame.grid_remove()

        # Track selections
        self.selected = {"seat": None, "time": None, "gate": None}

    def select_option(self, value, group):
        # Reset group
        button_list = {
            "seat": self.seat_buttons,
            "time": self.time_buttons,
            "gate": self.gate_buttons
        }[group]

        for btn in button_list:
            btn.configure(fg_color="#93DA97", text_color="#3E5F44")  # Reset to secondary green

        # Highlight selected
        for btn in button_list:
            if btn.cget("text") == value:
                btn.configure(fg_color="#3E5F44", text_color="#E8FFD7")  # Dark green with light green text

        # Store value
        self.selected[group] = value

    def open_modal(self):
        # If modal is already visible → hide it
        if self.orderFrame.winfo_ismapped():
            self.orderFrame.grid_remove()
            return

        # Else → show modal
        self.orderFrame.grid()
        for widget in self.orderFrame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.orderFrame,
            text="Order Status",
            font=("Book Antiqua", 24),
            text_color="#3E5F44",  # Dark green text
            anchor="nw"
        ).pack(pady=(25, 10), padx=10, anchor="w")

        ctk.CTkLabel(
            self.orderFrame,
            text=f"Tickets added\nSeat: {self.selected['seat']}\nTime: {self.selected['time']}\nGate: {self.selected['gate']}",
            font=("Book Antiqua", 16),
            text_color="#3E5F44",  # Dark green text
            anchor="w",
            justify="left"
        ).pack(pady=(10, 5), padx=20, anchor="w")

        # Ticket placeholder
        ctk.CTkFrame(
            self.orderFrame,
            fg_color="#93DA97",  # Secondary green for ticket placeholder
            height=100
        ).pack(fill="x", padx=20, pady=15)

        # Total and Checkout
        ctk.CTkLabel(
            self.orderFrame,
            text="Total: ₱300.00",  # Updated to peso symbol
            font=("Book Antiqua", 18),
            text_color="#3E5F44",  # Dark green text
            anchor="w"
        ).pack(pady=(10, 5), padx=20, anchor="w")

        ctk.CTkButton(
            self.orderFrame,
            text="Checkout",
            font=("Book Antiqua", 12),
            text_color="#E8FFD7",  # Light green text
            fg_color="#3E5F44",  # Dark green button
            hover_color="#5E936C",  # Hover green
            width=100,
            command=lambda: self.controller.show_frame("OrderCodeScreen")
        ).pack(pady=20)