import customtkinter as ctk

class OrderCodeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#E8FFD7")  # Light green background

        # Center content frame
        contentframe = ctk.CTkFrame(self, fg_color="#E8FFD7")  # Light green for content frame
        contentframe.place(relx=0.5, rely=0.5, anchor="center")  # Always center

        # Message
        label = ctk.CTkLabel(
            contentframe,
            text="YOUR ORDER CODE:",
            font=("Book Antiqua", 48, "bold"),
            text_color="#3E5F44",  # Dark green text
            justify="center"
        )
        label.pack(pady=(0, 10))

        # Order Code
        code = ctk.CTkLabel(
            contentframe,
            text="A1154H",
            font=("Book Antiqua", 45, "bold"),
            text_color="#3E5F44"  # Dark green text
        )
        code.pack(pady=(0, 40))

        # Button (modern style)
        button = ctk.CTkButton(
            contentframe,
            text="Order Again",
            font=("Book Antiqua", 18),
            fg_color="#3E5F44",  # Dark green button
            hover_color="#5E936C",  # Hover green
            text_color="#E8FFD7",  # Light green text
            corner_radius=10,
            width=200,
            height=50,
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=20)