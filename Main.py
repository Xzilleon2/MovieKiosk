import customtkinter as ctk
from Welcome_Screen import WelcomeScreen
from Home_Page import HomePage
from Selected import SelectedScreen
from OrderCode_Screen import OrderCodeScreen
from Admin_Page import AdminPage
from Sales_Page import SalesPage
from SalesHistory_Page import SalesHistoryPage


class MovieKiosk(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Movie Kiosk")
        self.attributes("-fullscreen", True)   # Fullscreen
        self.bind("<Escape>", lambda e: self.destroy())  # Exit with ESC

        # Main container (fills whole screen)
        self.container = ctk.CTkFrame(self, fg_color="black")
        self.container.pack(fill="both", expand=True)

        # Make container grid expandable
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Loop through all pages
        for F in (WelcomeScreen, HomePage, SelectedScreen,
                  OrderCodeScreen, AdminPage, SalesPage,
                  SalesHistoryPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame

            # Grid each frame so they overlap in same "cell"
            frame.grid(row=0, column=0, sticky="nsew")

        # Show first screen
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    # ✅ Set appearance & theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = MovieKiosk()
    app.mainloop()