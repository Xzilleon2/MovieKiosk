import customtkinter as ctk
import random
import string

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#E8FFD7")
        self.controller = controller

        contentframe = ctk.CTkFrame(self, fg_color="#E8FFD7")
        contentframe.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(
            contentframe,
            text="START\nTRANSACTION",
            font=("Book Antiqua", 48, "bold"),
            text_color="#3E5F44"
        )
        label.pack(pady=(0, 40))

        button = ctk.CTkButton(
            contentframe,
            text="View Movies",
            font=("Book Antiqua", 18),
            text_color="#E8FFD7",
            fg_color="#3E5F44",
            hover_color="#5E936C",
            corner_radius=8,
            width=200,
            height=50,
            command=self.start_transaction
        )
        button.pack(pady=10)

    def start_transaction(self):
        if not hasattr(self.controller, "last_code_number"):
            self.controller.last_code_number = 0
        self.controller.last_code_number += 1

        new_code = f"A{self.controller.last_code_number:03d}"
        self.controller.transaction_code = new_code
        print(f"[DEBUG] Generated transaction code: {new_code}")

        # ✅ Initialize the dictionary entry for this transaction
        self.controller.transactions[new_code] = []  # start empty list for tickets

        self.controller.show_frame("HomePage")
