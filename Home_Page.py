import os
import customtkinter as ctk
from Modals.Admin import admin_login_modal
from PIL import Image


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F4F4F4")
        self.controller = controller

        # Configure parent grid
        self.columnconfigure(0, weight=0)   # Left
        self.columnconfigure(1, weight=8)
        self.rowconfigure(0, weight=1)

        # ====================== MIDDLE CONTAINER ======================
        middleFrameCon = ctk.CTkFrame(self, fg_color="#F6F6F6")
        middleFrameCon.grid(row=0, column=1, sticky="nsew")
        middleFrameCon.rowconfigure(0, weight=1)
        middleFrameCon.rowconfigure(1, weight=1)
        middleFrameCon.rowconfigure(2, weight=4)
        middleFrameCon.columnconfigure(0, weight=1)

        # -------- Header --------
        upperFrame = ctk.CTkFrame(middleFrameCon, fg_color="#F6F6F6")
        upperFrame.grid(row=0, column=0, sticky="nsew", padx=50, pady=20)
        upperFrame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            upperFrame,
            text="Movie Ticketing Stand",
            font=("Book Antiqua", 36, "bold"),
            text_color="#665050"
        ).grid(row=0, column=0, sticky="nsew", pady=10)

        # ====================== SIDE MENU ======================
        sideFrame = ctk.CTkFrame(middleFrameCon, fg_color="#F6F6F6")
        sideFrame.grid(row=1, column=0, sticky="nsew")
        sideFrame.columnconfigure(0, weight=8)
        sideFrame.columnconfigure(1, weight=1)

        sideMenuCon = ctk.CTkFrame(sideFrame, fg_color="#F6F6F6")
        sideMenuCon.grid(row=0, column=0, sticky="nsew", padx=100, pady=(0, 20))
        for i in range(5):
            sideMenuCon.columnconfigure(i, weight=1)

        # Menu Buttons (with radius 10)
        menus = [
            ("Soon", "#FFFFFF"),
            ("Current", "#EFE9E0"),
            ("Previous", "#FFFFFF")
        ]
        for idx, (label, bgc) in enumerate(menus, start=1):
            ctk.CTkButton(
                sideMenuCon,
                text=label,
                font=("Book Antiqua", 14),
                text_color="#665050",
                fg_color=bgc,
                hover_color="#DDD",
                corner_radius=10
            ).grid(row=0, column=idx, sticky="nsew", padx=5)

        # ====================== ADMIN ICON ======================
        iconFrame = ctk.CTkFrame(self, fg_color="#F6F6F6")
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
            fg_color="#CD4126",
            hover_color="#C65D49",
            corner_radius=10,
            command=lambda: admin_login_modal(self, controller)
        ).pack(side="bottom", anchor="se", pady=15)

        # ====================== MOVIES GRID ======================
        middleFrame = ctk.CTkFrame(middleFrameCon, fg_color="#F6F6F6")
        middleFrame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(2):
            middleFrame.columnconfigure(i, weight=1)

        movies = [
            {"title": "Pet Sematary", "genre": "Horror|Thriller", "date": "September 5, 2025", "price": "$300"},
            {"title": "Inception", "genre": "Sci-Fi|Action", "date": "September 10, 2025", "price": "$500"},
            {"title": "Frozen II", "genre": "Animation|Adventure", "date": "September 15, 2025", "price": "$350"},
            {"title": "The Dark Knight", "genre": "Action|Drama", "date": "September 20, 2025", "price": "$450"}
        ]

        for idx, movie in enumerate(movies):
            row, col = divmod(idx, 2)
            self.create_movie_card(middleFrame, movie, row, col, controller)

    # Function to create movie cards dynamically
    def create_movie_card(self, parent, movie, row, col, controller):
        frame = ctk.CTkFrame(parent, fg_color="#F6F6F6")
        frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)

        # === Poster as CTkImage ===
        img_path = os.path.join(os.path.dirname(__file__), movie.get("poster", "Assets/PetSematary.png"))
        movie_img = ctk.CTkImage(light_image=Image.open(img_path), size=(200, 260))

        imgLabel = ctk.CTkLabel(frame, image=movie_img, text="", fg_color="#F6F6F6")
        imgLabel.image = movie_img
        imgLabel.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        infoFrame = ctk.CTkFrame(frame, fg_color="#F6F6F6")
        infoFrame.grid(row=0, column=1, sticky="nsew")
        infoFrame.columnconfigure(0, weight=1)

        (ctk.CTkLabel(infoFrame, text=movie["title"], font=("Book Antiqua", 24),
                     text_color="#665050", anchor="w")
         .grid(row=0, column=0, sticky="nsew",pady=10))

        (ctk.CTkLabel(infoFrame, text=movie["genre"], font=("Book Antiqua", 18),
                     text_color="#665050", anchor="w")
         .grid(row=1, column=0, sticky="nsew",pady=10))

        (ctk.CTkLabel(infoFrame, text=movie["date"], font=("Book Antiqua", 18),
                     text_color="#665050", anchor="w")
         .grid(row=2, column=0, sticky="nsew",pady=10))

        (ctk.CTkLabel(infoFrame, text=movie["price"], font=("Book Antiqua", 18),
                     text_color="#665050", anchor="w")
         .grid(row=3, column=0, sticky="nsew",pady=10))

        ctk.CTkButton(infoFrame, text="+", font=("Book Antiqua", 20),
                      text_color="#FFFFFF", fg_color="#CD4126", hover_color="#C65D49",
                      corner_radius=10, width=30, height=30,
                      command=lambda: controller.show_frame("SelectedScreen")
                      ).grid(row=4, column=0, sticky="w", pady=5)
