import tkinter as tk
from tkinter import PhotoImage
import os as os

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F4F4")

        #Main layout for admin page
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=1)

        # Side frame for column 1 ============================================================
        sideMenu = tk.Frame(
            self,
            bg="#F4F4F4",

        )
        sideMenu.grid(row=0, column=0, sticky="nsew", )
        sideMenu.rowconfigure(0, weight=1)
        sideMenu.columnconfigure(0, weight=1)

        #Frame Content for side Menu
        sideMenuCon = tk.Frame(
            sideMenu,
            bg="#FFFFFF",
            relief="groove",
        )
        sideMenuCon.grid(row=0, column=0, sticky="nsew", padx=(25, 5), pady=55)
        sideMenuCon.rowconfigure(0, weight=0)
        sideMenuCon.rowconfigure(1, weight=0)
        sideMenuCon.rowconfigure(2, weight=0)
        sideMenuCon.rowconfigure(3, weight=0)
        sideMenuCon.rowconfigure(4, weight=0)
        sideMenuCon.columnconfigure(0, weight=1)

        #Image path
        img_path = os.path.join(os.path.dirname(__file__), "Assets", "Bag.png")
        self.iconIMG = PhotoImage(file=img_path)

        # IMG LABEL
        imgLabel = tk.Label(
            sideMenuCon,
            bg="#FFFFFF",
            image=self.iconIMG,
        )
        imgLabel.grid(row=0, column=0, sticky="nsew", ipady=30)

        # Buttons for tables
        movieBtn = tk.Button(
            sideMenuCon,
            bg="#EFE9E0",
            text="Movies",
            font=("Book Antiqua", 16),
            fg="#665050",
            relief="flat",
        )
        movieBtn.grid(row=1, column=0, sticky="nsew", ipady=30)

        salesBtn = tk.Button(
            sideMenuCon,
            bg="#FFFFFF",
            text="Sales",
            font=("Book Antiqua", 16),
            fg="#665050",
            relief="flat",
        )
        salesBtn.grid(row=2, column=0, sticky="nsew", ipady=30)

        salesHistoryBtn = tk.Button(
            sideMenuCon,
            bg="#FFFFFF",
            text="Sales History",
            font=("Book Antiqua", 16),
            fg="#665050",
            relief="flat",
        )
        salesHistoryBtn.grid(row=3, column=0, sticky="nsew", ipady=30)

        logoutBtn = tk.Button(
            sideMenuCon,
            bg="#FFFFFF",
            text="Logout",
            font=("Book Antiqua", 16),
            fg="#665050",
            relief="flat",
        )
        logoutBtn.grid(row=4, column=0, sticky="nsew", ipady=30)

        # Main frame for tables ============================================================
        mainMenu = tk.Frame(
            self,
            bg="#F4F4F4",

        )
        mainMenu.grid(row=0, column=1, sticky="nsew", )
        mainMenu.rowconfigure(0, weight=1)
        mainMenu.columnconfigure(0, weight=1)

        # Frame container for tables
        mainMenuCon = tk.Frame(
            mainMenu,
            bg="#FFFFFF",
            relief="groove",
        )
        mainMenuCon .grid(row=0, column=0, sticky="nsew", padx=(5, 25), pady=55 )
        mainMenuCon .rowconfigure(0, weight=0)
        mainMenuCon .rowconfigure(1, weight=1)
        mainMenuCon .rowconfigure(2, weight=0)
        mainMenuCon .columnconfigure(0, weight=1)

        # Title Row
        Title = tk.Label(
            mainMenuCon,
            bg="#FFFFFF",
            text="MOVIE TICKETING ADMIN",
            font=("Book Antiqua", 30),
            fg="#665050",
            anchor="w",
        )
        Title.grid(row=0, column=0, sticky="nsew",ipady=30 ,padx=20)

        # Container for Buttons
        conBtn = tk.Frame(
            mainMenuCon,
            bg="#FFFFFF",
        )
        conBtn.grid(row=2, column=0, sticky="nsew", ipady=50)
        conBtn.rowconfigure(0, weight=1)
        conBtn.columnconfigure(0, weight=1)

        # register Movie
        registerBtn = tk.Button(
            conBtn,
            bg="#CD4126",
            text="Register",
            font=("Book Antiqua", 14),
            fg="#FFFFFF",
        )
        registerBtn.pack(side=tk.RIGHT, anchor=tk.NE, ipady=10, ipadx=80, padx=80)