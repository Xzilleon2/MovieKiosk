import customtkinter as ctk

class OrderCodeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#E8FFD7")
        self.controller = controller

        contentframe = ctk.CTkFrame(self, fg_color="#E8FFD7")
        contentframe.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(
            contentframe,
            text="YOUR ORDER CODE:",
            font=("Book Antiqua", 48, "bold"),
            text_color="#3E5F44"
        )
        label.pack(pady=(0, 10))

        # Store label as instance variable
        self.code_label = ctk.CTkLabel(
            contentframe,
            text="",
            font=("Book Antiqua", 45, "bold"),
            text_color="#3E5F44"
        )
        self.code_label.pack(pady=(0, 40))

        button = ctk.CTkButton(
            contentframe,
            text="Order Again",
            font=("Book Antiqua", 18),
            fg_color="#3E5F44",
            hover_color="#5E936C",
            text_color="#E8FFD7",
            corner_radius=10,
            width=200,
            height=50,
            command=lambda: controller.show_frame("WelcomeScreen")
        )
        button.pack(pady=20)

    def update_code(self):
        """Refresh code label each time this screen is shown."""
        code = self.controller.transaction_code or "N/A"
        print(f"[DEBUG] Updating code label → {code}")
        self.code_label.configure(text=code)
