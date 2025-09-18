import tkinter as tk

class OrderCodeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F4F4")

        # Center content frame
        contentframe = tk.Frame(self, bg="#F4F4F4")
        contentframe.place(relx=0.5, rely=0.5, anchor="center")  # Always center

        # Message
        label = tk.Label(
            contentframe,
            text=" YOUR ORDER CODE:",
            font=("Book Antiqua", 48, "bold"),
            bg="#F4F4F4",
            fg="#665050",
            justify="center"
        )
        label.pack(pady=(0, 10))

        # Order Code
        code = tk.Label(
            contentframe,
            text=" A1154H",
            font=("Book Antiqua", 45, "bold"),
            bg="#F4F4F4",
            fg="#665050",
            justify="center"
        )
        code.pack(pady=(0, 40))

        # Button (auto sizes to content, but centered)
        button = tk.Button(
            contentframe,
            text="Order Again",
            font=("Book Antiqua", 18),
            bg="#e07a5f",
            activebackground="#cc654a",
            activeforeground="white",
            relief="groove",
            fg="white",
            padx=40,
            pady=5,
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=10)
