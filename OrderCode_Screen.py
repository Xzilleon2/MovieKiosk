import customtkinter as ctk

class OrderCodeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F4F4F4")

        # Center content frame
        contentframe = ctk.CTkFrame(self, fg_color="#F4F4F4")
        contentframe.place(relx=0.5, rely=0.5, anchor="center")  # Always center

        # Message
        label = ctk.CTkLabel(
            contentframe,
            text="YOUR ORDER CODE:",
            font=("Book Antiqua", 48, "bold"),
            text_color="#665050"
        )
        label.pack(pady=(0, 10))

        # Order Code
        code = ctk.CTkLabel(
            contentframe,
            text="A1154H",
            font=("Book Antiqua", 45, "bold"),
            text_color="#665050"
        )
        code.pack(pady=(0, 40))

        # Button (modern style)
        button = ctk.CTkButton(
            contentframe,
            text="Order Again",
            font=("Book Antiqua", 18),
            fg_color="#e07a5f",
            hover_color="#cc654a",
            text_color="white",
            corner_radius=10,
            width=200,
            height=50,
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=20)
