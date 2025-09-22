import os
import tkinter as tk
from tkinter import PhotoImage
from Modals.Admin import admin_login_modal

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F4F4")
        self.controller = controller

        # Configure parent grid (2 columns, 1 row)
        self.columnconfigure(0, weight=1)   # Left
        self.columnconfigure(1, weight=8)   # Middle
        self.rowconfigure(0, weight=1) # 1 row

        # Side Frame  ======================================================================
        sideFrame = tk.Frame(
            self,
            relief=tk.SOLID,
            bg="#F6F6F6"
        )
        sideFrame.grid(row=0, column=0, sticky="nsew")
        sideFrame.columnconfigure(0, weight=1) # make the column expand
        sideFrame.rowconfigure(0, weight=8) # make the row expand
        sideFrame.rowconfigure(1, weight=1) # make the row expand

        sideMenuCon = tk.Frame(
            sideFrame,
            bg="#FFFFFF",
            relief=tk.RAISED,
        )
        sideMenuCon.grid(row=0, column=0, sticky="nsew", pady=(115,50), padx=35)
        sideMenuCon.rowconfigure(0, weight=3) # row 1 responsive
        sideMenuCon.rowconfigure(1, weight=2) # row 2 responsive
        sideMenuCon.rowconfigure(2, weight=2) # row 3 responsive
        sideMenuCon.rowconfigure(3, weight=2) # row 4 responsive
        sideMenuCon.rowconfigure(4, weight=3) # row 5 responsive
        sideMenuCon.columnconfigure(0, weight=1)  # column responsive

        btnupComing = tk.Button(
            sideMenuCon,
            text="UPCOMING",
            font=("Book Antiqua", 14),
            fg="#665050",
            bg="#FFFFFF",
            relief=tk.FLAT
        )
        btnupComing.grid(row=1, column=0, sticky="nsew")

        btnCurrent = tk.Button(
            sideMenuCon,
            text="Current",
            font=("Book Antiqua", 14),
            fg="#665050",
            bg="#EFE9E0",
            relief=tk.FLAT
        )
        btnCurrent.grid(row=2, column=0, sticky="nsew")

        btnPrevoius = tk.Button(
            sideMenuCon,
            text="Previous",
            font=("Book Antiqua", 14),
            fg="#665050",
            bg="#FFFFFF",
            relief=tk.FLAT

        )
        btnPrevoius.grid(row=3, column=0, sticky="nsew")

        iconFrame = tk.Frame(
            sideFrame,
            bg="#F6F6F6",
        )
        iconFrame.grid(row=1, column=0, sticky="nsew", pady=15, padx=35)
        iconFrame.columnconfigure(0, weight=1)
        iconFrame.rowconfigure(0, weight=1)

        #button admin
        #Image path
        img_path = os.path.join(os.path.dirname(__file__), "Assets", "person.png")
        self.iconIMG = PhotoImage(file=img_path)

        icon = tk.Button(
            iconFrame,
            height=36,
            width=36,
            image=self.iconIMG,
            bg="#CD4126",
            activebackground="#C65D49",
            command=lambda: admin_login_modal(self, controller)
        )
        icon.pack(side=tk.LEFT, anchor="s")

        # Middle Frame ======================================================================
        middleFrame = tk.Frame(
            self,
            relief=tk.SOLID,
            bg="#F6F6F6"
        )
        middleFrame.grid(row=0, column=1, sticky="nsew")
        middleFrame.rowconfigure(0, weight=2)    # Make sure row1 expands
        middleFrame.rowconfigure(1, weight=2)    # Make sure row2 expands
        middleFrame.columnconfigure(0, weight=1) # Make sure column expands

        #Upper Frame
        upperFrame = tk.Frame(
            middleFrame,
            bg="#F6F6F6"
        )
        upperFrame.grid(row=0, column=0, sticky="nsew")
        upperFrame.columnconfigure(0, weight=5) # column 1 responsive
        upperFrame.columnconfigure(1, weight=2) # column 2 responsive
        upperFrame.columnconfigure(2, weight=2) # column 3 responsive
        upperFrame.columnconfigure(3, weight=3) # column 4 responsive
        upperFrame.rowconfigure(0, weight=1)  # row responsive

        TitleLabel = tk.Label(
            upperFrame,
            text="Movie Ticketing Stand",
            font=("Book Antiqua", 35),
            fg="#665050",
            bg="#F6F6F6",
            anchor="w",
        )
        TitleLabel.grid(row=0, column=0, sticky="nsew")

        DateLabel = tk.Label(
            upperFrame,
            text="September 5, 2025",
            font=("Book Antiqua", 15),
            fg="#665050",
            bg="#F6F6F6",
            anchor="e",
        )
        DateLabel.grid(row=0, column=1, sticky="nsew")

        #Frame for the button
        iconFrameBag = tk.Frame(
            upperFrame,
            bg="#F6F6F6",
        )
        iconFrameBag.grid(row=0, column=2, sticky="nsew", padx=15)

        #Image path
        img_path = os.path.join(os.path.dirname(__file__), "Assets", "Ticket.png")
        self.iconBagIMG = PhotoImage(file=img_path)

        iconBag = tk.Button(
            iconFrameBag,
            image=self.iconBagIMG,
            bg="#F6F6F6",
            relief=tk.FLAT,
        )
        iconBag.pack(side="left")

        # Middle Frame
        middleFrame = tk.Frame(
            middleFrame,
            bg="#F6F6F6"
        )
        middleFrame.grid(row=1, column=0, sticky="nsew")
        middleFrame.columnconfigure(0, weight=2) # column 1 responsive
        middleFrame.columnconfigure(1, weight=2) # column 2 responsive
        middleFrame.rowconfigure(0, weight=2) # row 1 responsive
        middleFrame.rowconfigure(1, weight=2) # row 2 responsive

        #Contents =================================================================

        #content 1
        movie1 = tk.Frame(
            middleFrame,
            bg="#F6F6F6"
        )
        movie1.grid(row=0, column=0, sticky="nw")
        movie1.columnconfigure(0, weight=0)
        movie1.columnconfigure(1, weight=0)
        movie1.rowconfigure(0, weight=1)

        #path for movie image
        movie1_IMG = os.path.join(os.path.dirname(__file__), "Assets", "PetSematary.png")
        self.movieIMG = PhotoImage(file=movie1_IMG)

        #movie image label
        imgLabel = tk.Label(
            movie1,
            image=self.movieIMG,
            bg="#F6F6F6",
            relief=tk.RIDGE,
        )
        imgLabel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        #Movie Info
        contentFrame= tk.Frame(
            movie1,
            bg="#F6F6F6"
        )
        contentFrame.grid(row=0, column=1, sticky="nsew")
        contentFrame.rowconfigure(0, weight=3)
        contentFrame.rowconfigure(1, weight=2)
        contentFrame.rowconfigure(2, weight=2)
        contentFrame.rowconfigure(3, weight=2)
        contentFrame.rowconfigure(4, weight=2)
        contentFrame.columnconfigure(0, weight=1)

        title = tk.Label(
            contentFrame,
            text="Pet Sematary",
            font=("Book Antiqua", 28),
            fg="#665050",
            anchor="nw",
            bg="#F6F6F6"
        )
        title.grid(row=0, column=0, sticky="nsew")

        genre = tk.Label(
            contentFrame,
            text="Horror|Thriller",
            font=("Book Antiqua", 18),
            fg="#665050",
            anchor="sw",
            bg="#F6F6F6"
        )
        genre.grid(row=1, column=0, sticky="nsew")

        date = tk.Label(
            contentFrame,
            text="September 5, 2025",
            font=("Book Antiqua", 18),
            fg="#665050",
            anchor="nw",
            bg="#F6F6F6"
        )
        date.grid(row=2, column=0, sticky="nsew")

        price = tk.Label(
            contentFrame,
            text="$300",
            font=("Book Antiqua", 18),
            fg="#665050",
            anchor="w",
            bg="#F6F6F6"
        )
        price.grid(row=3, column=0, sticky="nsew")

        BtnFrame = tk.Frame(
            contentFrame,
            bg="#F6F6F6"
        )
        BtnFrame.grid(row=4, column=0, sticky="nsew")

        addBtn = tk.Button(
            BtnFrame,
            text="+",
            width=2,
            height=1,
            font=("Book Antiqua", 14),
            fg="#FFFFFF",
            bg="#CD4126",
            activebackground="#C65D49",
            activeforeground="#FFFFFF",
            command= lambda:controller.show_frame("SelectedScreen")
        )
        addBtn.grid(row=4, column=0, sticky="nsew", ipadx=2)

        #==========================================================================
        #content 2
        movie2 = tk.Frame(
            middleFrame,
            bg="#F6F6F6"
        )
        movie2.grid(row=0, column=1, sticky="nw")
        movie2.columnconfigure(0, weight=0)
        movie2.columnconfigure(1, weight=0)
        movie2.rowconfigure(0, weight=1)

        #path for movie image
        movie2_IMG = os.path.join(os.path.dirname(__file__), "Assets", "PetSematary.png")
        self.movieIMG2 = PhotoImage(file=movie2_IMG)

        #movie image label
        imgLabel2 = tk.Label(
            movie2,
            image=self.movieIMG2,
            bg="#F6F6F6",
            relief=tk.RIDGE,
        )
        imgLabel2.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        #Movie Info
        contentFrame2 = tk.Frame(
            movie2,
            bg="#F6F6F6"
        )
        contentFrame2.grid(row=0, column=1, sticky="nsew")
        contentFrame2.rowconfigure(0, weight=3)
        contentFrame2.rowconfigure(1, weight=2)
        contentFrame2.rowconfigure(2, weight=2)
        contentFrame2.rowconfigure(3, weight=2)
        contentFrame2.rowconfigure(4, weight=2)
        contentFrame2.columnconfigure(0, weight=1)

        title2 = tk.Label(
            contentFrame2,
            text="Pet Sematary",
            font=("Book Antiqua", 28),
            fg="#665050",
            anchor="nw",
            bg="#F6F6F6"
        )
        title2.grid(row=0, column=0, sticky="nsew")

        genre2 = tk.Label(
            contentFrame2,
            text="Horror|Thriller",
            font=("Book Antiqua", 18),
            fg="#665050",
            anchor="sw",
            bg="#F6F6F6"
        )
        genre2.grid(row=1, column=0, sticky="nsew")

        date2 = tk.Label(
            contentFrame2,
            text="September 5, 2025",
            font=("Book Antiqua", 18),
            fg="#665050",
            anchor="nw",
            bg="#F6F6F6"
        )
        date2.grid(row=2, column=0, sticky="nsew")

        price2 = tk.Label(
            contentFrame2,
            text="$300",
            font=("Book Antiqua", 18),
            fg="#665050",
            anchor="w",
            bg="#F6F6F6"
        )
        price2.grid(row=3, column=0, sticky="nsew")

        BtnFrame2 = tk.Frame(
            contentFrame2,
            bg="#F6F6F6"
        )
        BtnFrame2.grid(row=4, column=0, sticky="nsew")

        addBtn2 = tk.Button(
            BtnFrame2,
            text="+",
            width=2,
            height=1,
            font=("Book Antiqua", 14),
            fg="#FFFFFF",
            bg="#CD4126",
            activebackground="#C65D49",
        activeforeground = "#FFFFFF"
        )
        addBtn2.grid(row=4, column=0, sticky="nsew", ipadx=2)

        #==========================================================================
        #content 3
        movie3 = tk.Frame(
            middleFrame,
            bg="#F6F6F6"
        )
        movie3.grid(row=1, column=0, sticky="nw")
        movie3.columnconfigure(0, weight=0)
        movie3.columnconfigure(1, weight=0)
        movie3.rowconfigure(0, weight=1)

        #path for movie image
        movie3_IMG = os.path.join(os.path.dirname(__file__), "Assets", "PetSematary.png")
        self.movieIMG3 = PhotoImage(file=movie2_IMG)

        #movie image label
        imgLabel3 = tk.Label(
            movie3,
            image=self.movieIMG3,
            bg="#F6F6F6",
            relief=tk.RIDGE,
        )
        imgLabel3.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        #Movie Info
        contentFrame3 = tk.Frame(
            movie3,
            bg="#F6F6F6"
        )
        contentFrame3.grid(row=0, column=1, sticky="nsew")
        contentFrame3.rowconfigure(0, weight=3)
        contentFrame3.rowconfigure(1, weight=2)
        contentFrame3.rowconfigure(2, weight=2)
        contentFrame3.rowconfigure(3, weight=2)
        contentFrame3.rowconfigure(4, weight=2)
        contentFrame3.columnconfigure(0, weight=1)

        title3 = tk.Label(
            contentFrame3,
            text="Pet Sematary",
            font=("Book Antiqua", 28),
            fg="#665050",
            anchor="nw",
            bg="#F6F6F6"
        )
        title3.grid(row=0, column=0, sticky="nsew")

        genre3 = tk.Label(
            contentFrame3,
            text="Horror|Thriller",
            font=("Book Antiqua", 18),
            fg="#665050",
            anchor="sw",
            bg="#F6F6F6"
        )
        genre3.grid(row=1, column=0, sticky="nsew")

        date3 = tk.Label(
            contentFrame3,
            text="September 5, 2025",
            font=("Book Antiqua", 18),
            fg="#665050",
            anchor="nw",
            bg="#F6F6F6"
        )
        date3.grid(row=2, column=0, sticky="nsew")

        price3 = tk.Label(
            contentFrame3,
            text="$300",
            font=("Book Antiqua", 18),
            fg="#665050",
            anchor="w",
            bg="#F6F6F6"
        )
        price3.grid(row=3, column=0, sticky="nsew")

        BtnFrame3 = tk.Frame(
            contentFrame3,
            bg="#F6F6F6"
        )
        BtnFrame3.grid(row=4, column=0, sticky="nsew")

        addBtn3 = tk.Button(
            BtnFrame3,
            text="+",
            width=2,
            height=1,
            font=("Book Antiqua", 14),
            fg="#FFFFFF",
            bg="#CD4126",
            activebackground="#C65D49",
        activeforeground = "#FFFFFF"
        )
        addBtn3.grid(row=4, column=0, sticky="nsew", ipadx=2)

        #==========================================================================