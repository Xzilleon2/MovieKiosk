import os
import customtkinter as ctk
from Modals.Admin import admin_login_modal
from PIL import Image
from Classes.MoviesView_Class import MoviesView

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#E8FFD7")  # Light green background
        self.controller = controller

        # Configure parent grid
        self.columnconfigure(0, weight=0)  # Left
        self.columnconfigure(1, weight=8)
        self.rowconfigure(0, weight=1)

        # ====================== MIDDLE CONTAINER ======================
        middleFrameCon = ctk.CTkFrame(self, fg_color="#E8FFD7")  # Light green background
        middleFrameCon.grid(row=0, column=1, sticky="nsew")
        middleFrameCon.rowconfigure(0, weight=1)
        middleFrameCon.rowconfigure(1, weight=1)
        middleFrameCon.rowconfigure(2, weight=4)
        middleFrameCon.columnconfigure(0, weight=1)

        # -------- Header --------
        upperFrame = ctk.CTkFrame(middleFrameCon, fg_color="#E8FFD7")  # Light green background
        upperFrame.grid(row=0, column=0, sticky="nsew", padx=50, pady=20)
        upperFrame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            upperFrame,
            text="Movie Ticketing Stand",
            font=("Book Antiqua", 36, "bold"),
            text_color="#3E5F44"  # Dark green text
        ).grid(row=0, column=0, sticky="nsew", pady=10)

        # ====================== SIDE MENU ======================
        sideFrame = ctk.CTkFrame(middleFrameCon, fg_color="#E8FFD7")  # Light green background
        sideFrame.grid(row=1, column=0, sticky="nsew")
        sideFrame.columnconfigure(0, weight=8)
        sideFrame.columnconfigure(1, weight=1)

        sideMenuCon = ctk.CTkFrame(sideFrame, fg_color="#E8FFD7")  # Light green background
        sideMenuCon.grid(row=0, column=0, sticky="nsew", padx=100, pady=(0, 20))
        for i in range(5):
            sideMenuCon.columnconfigure(i, weight=1)

        # Menu Buttons (with radius 10)
        menus = [
            ("Soon", "#E8FFD7"),  # Light green background
            ("Current", "#93DA97"),  # Secondary green for selected
            ("Previous", "#E8FFD7")  # Light green background
        ]
        for idx, (label, bgc) in enumerate(menus, start=1):
            ctk.CTkButton(
                sideMenuCon,
                text=label,
                font=("Book Antiqua", 14),
                text_color="#3E5F44",  # Dark green text
                border_color="#3E5F44",
                border_width=1,
                fg_color=bgc,
                hover_color="#5E936C",  # Hover green
                corner_radius=10,
            ).grid(row=0, column=idx, sticky="nsew", padx=5, ipady=5)

        # ====================== ADMIN ICON ======================
        iconFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")  # Light green background
        iconFrame.grid(row=0, column=0, sticky="nsew", ipadx=10)
        iconFrame.rowconfigure(0, weight=1)
        iconFrame.columnconfigure(0, weight=1)

        img_path = os.path.join(os.path.dirname(__file__), "Assets", "person.png")
        self.iconIMG = ctk.CTkImage(light_image=Image.open(img_path), size=(20, 20))

        ctk.CTkButton(
            iconFrame,
            width=36,
            height=36,
            image=self.iconIMG,
            text="",
            fg_color="#3E5F44",  # Dark green button
            hover_color="#5E936C",  # Hover green
            corner_radius=10,
            command=lambda: admin_login_modal(self, controller)
        ).pack(side="bottom", anchor="se", pady=15)

        # ====================== MOVIES GRID ======================
        middleFrame = ctk.CTkFrame(middleFrameCon, fg_color="#E8FFD7")  # Light green background
        middleFrame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(2):
            middleFrame.columnconfigure(i, weight=1)

        # ✅ Fetch movies from DB
        mv = MoviesView()
        movies = mv.getMoviesThisMonth()

        # If no movies, display a fallback label
        if not movies:
            ctk.CTkLabel(
                middleFrame,
                text="No movies available this month.",
                font=("Book Antiqua", 20),
                text_color="#3E5F44"  # Dark green text
            ).grid(row=0, column=0, pady=20)
        else:
            for idx, movie in enumerate(movies):
                row, col = divmod(idx, 2)
                self.create_movie_card(middleFrame, movie, row, col, controller)

    def create_movie_card(self, parent, movie, row, col, controller):
        frame = ctk.CTkFrame(parent, fg_color="#E8FFD7")  # Light green background
        frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)

        # === Poster with Shadow ===
        img_path = os.path.join(os.path.dirname(__file__), "Assets", "Posters", movie["poster"])
        movie_img = ctk.CTkImage(light_image=Image.open(img_path), size=(200, 260))

        # Create a shadow frame
        shadow_frame = ctk.CTkFrame(
            frame,
            fg_color="#E8FFD7",  # Match background to blend
            border_color="#3E5F44",  # Dark green for shadow effect
            border_width=2,
            corner_radius=8
        )
        shadow_frame.grid(row=0, column=0, sticky="n", padx=(12, 10), pady=(12, 10))

        imgLabel = ctk.CTkLabel(
            shadow_frame,
            image=movie_img,
            text="",
            fg_color="#E8FFD7"  # Light green to match background
        )
        imgLabel.image = movie_img
        imgLabel.pack(padx=4, pady=4)  # Padding inside shadow frame

        infoFrame = ctk.CTkFrame(frame, fg_color="#E8FFD7")  # Light green background
        infoFrame.grid(row=0, column=1, sticky="nsew")
        infoFrame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            infoFrame,
            text=movie["title"],
            font=("Book Antiqua", 24),
            text_color="#3E5F44",  # Dark green text
            wraplength=250,
            anchor="w"
        ).grid(row=0, column=0, sticky="nsew", pady=10)

        ctk.CTkLabel(
            infoFrame,
            text=movie["genre"],
            font=("Book Antiqua", 18),
            text_color="#3E5F44",  # Dark green text
            anchor="w"
        ).grid(row=1, column=0, sticky="nsew", pady=10)

        ctk.CTkLabel(
            infoFrame,
            text=movie["date"],
            font=("Book Antiqua", 18),
            text_color="#3E5F44",  # Dark green text
            anchor="w"
        ).grid(row=2, column=0, sticky="nsew", pady=10)

        ctk.CTkLabel(
            infoFrame,
            text=f"₱{movie['price']:.2f}",  # Format price with peso sign
            font=("Book Antiqua", 18),
            text_color="#3E5F44",  # Dark green text
            anchor="w"
        ).grid(row=3, column=0, sticky="nsew", pady=10)

        ctk.CTkButton(
            infoFrame,
            text="+",
            font=("Book Antiqua", 20),
            text_color="#E8FFD7",  # Light green text
            fg_color="#3E5F44",  # Dark green button
            hover_color="#5E936C",  # Hover green
            corner_radius=10,
            width=30,
            height=30,
            command=lambda: controller.show_frame("SelectedScreen")
        ).grid(row=4, column=0, sticky="w", pady=5)