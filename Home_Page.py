import os
import tkinter as tk
from tkinter import PhotoImage
from Modals.Admin import admin_login_modal
from PIL import Image, ImageTk


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F4F4")
        self.controller = controller

        # Configure parent grid (2 columns, 1 row)
        self.columnconfigure(0, weight=1)   # Left
        self.columnconfigure(1, weight=8)   # Middle
        self.rowconfigure(0, weight=1)      # Main row

        # ====================== SIDE MENU ======================
        sideFrame = tk.Frame(self, bg="#F6F6F6")
        sideFrame.grid(row=0, column=0, sticky="nsew")
        sideFrame.columnconfigure(0, weight=1)
        sideFrame.rowconfigure(0, weight=8)
        sideFrame.rowconfigure(1, weight=1)

        # Side menu container
        sideMenuCon = tk.Frame(sideFrame, bg="#FFFFFF", relief=tk.RAISED)
        sideMenuCon.grid(row=0, column=0, sticky="nsew", pady=(115, 50), padx=35)
        for i in range(5):
            sideMenuCon.rowconfigure(i, weight=1)
        sideMenuCon.columnconfigure(0, weight=1)

        # Menu Buttons
        menus = [
            ("UPCOMING", "#FFFFFF"),
            ("Current", "#EFE9E0"),
            ("Previous", "#FFFFFF")
        ]
        for idx, (label, bgc) in enumerate(menus, start=1):
            tk.Button(
                sideMenuCon,
                text=label,
                font=("Book Antiqua", 14),
                fg="#665050",
                bg=bgc,
                relief=tk.FLAT
            ).grid(row=idx, column=0, sticky="nsew")

        # Admin Icon
        iconFrame = tk.Frame(sideFrame, bg="#F6F6F6")
        iconFrame.grid(row=1, column=0, sticky="nsew", pady=15, padx=35)
        iconFrame.columnconfigure(0, weight=1)

        img_path = os.path.join(os.path.dirname(__file__), "Assets", "person.png")
        self.iconIMG = PhotoImage(file=img_path)
        tk.Button(
            iconFrame,
            height=36,
            width=36,
            image=self.iconIMG,
            bg="#CD4126",
            activebackground="#C65D49",
            command=lambda: admin_login_modal(self, controller)
        ).pack(side=tk.LEFT, anchor="s")

        # ====================== MIDDLE CONTAINER ======================
        middleFrameCon = tk.Frame(self, bg="#F6F6F6")
        middleFrameCon.grid(row=0, column=1, sticky="nsew")
        middleFrameCon.rowconfigure(0, weight=1)
        middleFrameCon.rowconfigure(1, weight=4)
        middleFrameCon.columnconfigure(0, weight=1)

        # -------- Header --------
        upperFrame = tk.Frame(middleFrameCon, bg="#F6F6F6")
        upperFrame.grid(row=0, column=0, sticky="nsew", padx=50, pady=10)
        for c in range(4):
            upperFrame.columnconfigure(c, weight=1)

        tk.Label(
            upperFrame,
            text="Movie Ticketing Stand",
            font=("Book Antiqua", 28),
            fg="#665050",
            bg="#F6F6F6",
            anchor="w"
        ).grid(row=0, column=0, sticky="nsew")

        tk.Label(
            upperFrame,
            text="September 5, 2025",
            font=("Book Antiqua", 15),
            fg="#665050",
            bg="#F6F6F6",
            anchor="e"
        ).grid(row=0, column=1, sticky="nsew")

        # Ticket Bag
        img_path = os.path.join(os.path.dirname(__file__), "Assets", "Ticket.png")
        self.iconBagIMG = PhotoImage(file=img_path)
        tk.Button(
            upperFrame,
            image=self.iconBagIMG,
            bg="#F6F6F6",
            relief=tk.FLAT
        ).grid(row=0, column=2, sticky="w", padx=15)

        # -------- Movies Grid --------
        middleFrame = tk.Frame(middleFrameCon, bg="#F6F6F6")
        middleFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Grid responsiveness (2 cols, multiple rows)
        for i in range(2):
            middleFrame.columnconfigure(i, weight=1)

        # Movie data list (dynamic)
        movies = [
            {"title": "Pet Sematary", "genre": "Horror|Thriller", "date": "September 5, 2025", "price": "$300"},
            {"title": "Inception", "genre": "Sci-Fi|Action", "date": "September 10, 2025", "price": "$500"},
            {"title": "Frozen II", "genre": "Animation|Adventure", "date": "September 15, 2025", "price": "$350"},
            {"title": "The Dark Knight", "genre": "Action|Drama", "date": "September 20, 2025", "price": "$450"}
        ]

        # Dynamically create movie cards
        for idx, movie in enumerate(movies):
            row, col = divmod(idx, 2)  # 2 columns
            self.create_movie_card(middleFrame, movie, row, col, controller)

    # Function to create movie cards dynamically
    def create_movie_card(self, parent, movie, row, col, controller):
        frame = tk.Frame(parent, bg="#F6F6F6", relief=tk.RIDGE)
        frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)
        frame.rowconfigure(0, weight=1)

        # === Resize Poster ===
        img_path = os.path.join(os.path.dirname(__file__), movie.get("poster", "Assets/PetSematary.png"))
        img = Image.open(img_path)

        # Resize to fit (adjust size as needed)
        img = img.resize((180, 250), Image.LANCZOS)

        movie_img = ImageTk.PhotoImage(img)

        imgLabel = tk.Label(frame, image=movie_img, bg="#F6F6F6")
        imgLabel.image = movie_img  # prevent garbage collection
        imgLabel.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        # Info
        infoFrame = tk.Frame(frame, bg="#F6F6F6")
        infoFrame.grid(row=0, column=1, sticky="nsew")
        for i in range(5):
            infoFrame.rowconfigure(i, weight=1)
        infoFrame.columnconfigure(0, weight=1)

        tk.Label(infoFrame, text=movie["title"], font=("Book Antiqua", 20),
                 fg="#665050", bg="#F6F6F6", anchor="w").grid(row=0, column=0, sticky="nsew")

        tk.Label(infoFrame, text=movie["genre"], font=("Book Antiqua", 14),
                 fg="#665050", bg="#F6F6F6", anchor="w").grid(row=1, column=0, sticky="nsew")

        tk.Label(infoFrame, text=movie["date"], font=("Book Antiqua", 14),
                 fg="#665050", bg="#F6F6F6", anchor="w").grid(row=2, column=0, sticky="nsew")

        tk.Label(infoFrame, text=movie["price"], font=("Book Antiqua", 14),
                 fg="#665050", bg="#F6F6F6", anchor="w").grid(row=3, column=0, sticky="nsew")

        tk.Button(infoFrame, text="+", font=("Book Antiqua", 14),
                  fg="#FFFFFF", bg="#CD4126", activebackground="#C65D49",
                  command=lambda: controller.show_frame("SelectedScreen")
                  ).grid(row=4, column=0, sticky="w", pady=5)
