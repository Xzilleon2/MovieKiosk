import customtkinter as ctk

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F4F4F4")

        # Center content frame
        contentframe = ctk.CTkFrame(self, fg_color="#F4F4F4")
        contentframe.place(relx=0.5, rely=0.5, anchor="center")  # Always center

        # Transaction Message
        label = ctk.CTkLabel(
            contentframe,
            text=" START\nTRANSACTION",
            font=("Book Antiqua", 48, "bold"),
            text_color="#665050",
            justify="center"
        )
        label.pack(pady=(0, 40))

        # Button (auto sizes to content, but centered)
        button = ctk.CTkButton(
            contentframe,
            text="View Movies",
            font=("Book Antiqua", 18),
            text_color="white",
            fg_color="#e07a5f",
            hover_color="#cc654a",
            corner_radius=8,
            width=200,   # optional fixed width
            height=50,   # optional fixed height
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=10)
