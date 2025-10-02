import customtkinter as ctk

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#E8FFD7")  # Light green background

        # Center content frame
        contentframe = ctk.CTkFrame(self, fg_color="#E8FFD7")
        contentframe.place(relx=0.5, rely=0.5, anchor="center")  # Always center

        # Transaction Message
        label = ctk.CTkLabel(
            contentframe,
            text="START\nTRANSACTION",
            font=("Book Antiqua", 48, "bold"),
            text_color="#3E5F44",  # Dark green text
            justify="center"
        )
        label.pack(pady=(0, 40))

        # Button (auto sizes to content, but centered)
        button = ctk.CTkButton(
            contentframe,
            text="View Movies",
            font=("Book Antiqua", 18),
            text_color="#E8FFD7",  # Light green text
            fg_color="#3E5F44",  # Dark green button
            hover_color="#5E936C",  # Hover green
            corner_radius=8,
            width=200,  # Fixed width
            height=50,  # Fixed height
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=10)