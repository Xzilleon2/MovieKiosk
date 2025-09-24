import tkinter as tk
from tkinter import ttk, PhotoImage
import os
from Modals.Register import register_modal
from Styles.Table import setup_table_style, zebra_striping, sort_table, disable_resize

class SalesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F4F4")

        # Apply global Table styles
        setup_table_style()

        #Main layout for sales page
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=1)

        #Frame Content for side Menu
        sideMenuCon = tk.Frame(self, bg="#FFFFFF", relief="groove")
        sideMenuCon.grid(row=0, column=0, sticky="nsew")
        sideMenuCon.columnconfigure(0, weight=1)

        #Image path
        img_path = os.path.join(os.path.dirname(__file__), "Assets", "Bag.png")
        self.iconIMG = PhotoImage(file=img_path)

        # IMG LABEL
        imgLabel = tk.Label(sideMenuCon, bg="#FFFFFF", image=self.iconIMG)
        imgLabel.grid(row=0, column=0, sticky="nsew", pady=(60,20))

        # Buttons & Labels for sideBar
        tablesLabel = tk.Label(sideMenuCon, bg="#FFFFFF", text="TABLES",
                               font=("Book Antiqua", 12), fg="#665050")
        tablesLabel.grid(row=1, column=0, sticky="nsw", ipady=15, ipadx=10)

        movieBtn = tk.Button(sideMenuCon, bg="#FFFFFF", text="Movies",
                             font=("Book Antiqua", 12), fg="#665050", relief="flat",
                             command=lambda: controller.show_frame("AdminPage"))
        movieBtn.grid(row=2, column=0, sticky="nsew", ipady=10)

        salesBtn = tk.Button(sideMenuCon, bg="#EFE9E0", text="Sales",
                             font=("Book Antiqua", 12), fg="#665050", relief="flat")
        salesBtn.grid(row=3, column=0, sticky="nsew", ipady=10)

        salesHistoryBtn = tk.Button(sideMenuCon, bg="#FFFFFF", text="Sales History",
                                    font=("Book Antiqua", 12), fg="#665050", relief="flat",
                                    command=lambda: controller.show_frame("SalesHistoryPage"))
        salesHistoryBtn.grid(row=4, column=0, sticky="nsew", ipady=10)

        optionsLabel = tk.Label(sideMenuCon, bg="#FFFFFF", text="OPTION",
                                font=("Book Antiqua", 12), fg="#665050")
        optionsLabel.grid(row=5, column=0, sticky="nsw", ipady=15, ipadx=10)

        logoutBtn = tk.Button(sideMenuCon, bg="#FFFFFF", text="Logout",
                              font=("Book Antiqua", 12), fg="#665050", relief="flat")
        logoutBtn.grid(row=6, column=0, sticky="nsew", ipady=10)

        # Main frame for tables ============================================================
        mainMenu = tk.Frame(self, bg="#F4F4F4")
        mainMenu.grid(row=0, column=1, sticky="nsew")
        mainMenu.rowconfigure(0, weight=0)
        mainMenu.rowconfigure(1, weight=1)
        mainMenu.columnconfigure(0, weight=1)

        # Frame container for tables
        mainMenuCon = tk.Frame(mainMenu, bg="#FFFFFF", relief="groove")
        mainMenuCon.grid(row=1, column=0, sticky="nsew", padx=25, pady=35)
        mainMenuCon.rowconfigure(0, weight=0)
        mainMenuCon.rowconfigure(1, weight=0)
        mainMenuCon.rowconfigure(2, weight=0)
        mainMenuCon.rowconfigure(3, weight=3)
        mainMenuCon.columnconfigure(0, weight=1)

        # Title Row =====================================================================
        Title = tk.Label(mainMenuCon, bg="#FFFFFF", text="SALES TABLE",
                         font=("Book Antiqua", 18), fg="#665050", anchor="sw")
        Title.grid(row=0, column=0, sticky="nsew", padx= 25, ipady=15)
        Title.columnconfigure(0, weight=1)

        subTitle = tk.Label(mainMenuCon, bg="#FFFFFF", text="Display in queue payments.",
                            font=("Book Antiqua", 12), fg="#665050", anchor="nw")
        subTitle.grid(row=1, column=0, sticky="nsew", padx= 25)

        # Container for Table =====================================================================
        tableCon = tk.Frame(mainMenuCon, bg="#FFFFFF")
        tableCon.grid(row=3, column=0, sticky="nsew", pady=10)

        # --- Table ---
        table = ttk.Treeview(
            tableCon,
            columns=('ID', 'CODE', 'Seat', 'Price', 'Genre', 'Date'),
            show='headings',
            style="Custom.Treeview"
        )

        for col in ('ID', 'CODE', 'Seat', 'Price', 'Genre', 'Date'):
            table.heading(col, text=col, anchor='center')

        table.pack(expand=True, fill="both", padx=20)

        # Column alignment
        table.column('ID', anchor='e', width=80)
        table.column('CODE', anchor='w', width=200)
        table.column('Seat', anchor='w', width=300, stretch=False)
        table.column('Price', anchor='e', width=100)
        table.column('Genre', anchor='w', width=150)
        table.column('Date', anchor='w', width=150)

        # Apply zebra striping
        zebra_striping(table)

        # Disable resize
        table.bind("<Button-1>", lambda e: disable_resize(e, table))

        # Table Sample Data
        content = ['001', 'Pet Sematary', 'visiting their old house in...', '$300',
                   'Horror|Thriller', 'November 5, 2025']

        # Random content
        for i in range(15):
            table.insert(parent='', index=0, values=content)

        # Container for Buttons ================================================================
        conBtn = tk.Frame(mainMenuCon, bg="#FFFFFF")
        conBtn.grid(row=2, column=0, sticky="nsew", ipady=10)
        conBtn.columnconfigure(0, weight=1)
        conBtn.columnconfigure(1, weight=1)
        conBtn.rowconfigure(0, weight=1)

        # --- Search Bar --------------------------------------------------------------------------
        searchCon = tk.Frame(conBtn, bg="#FFFFFF")
        searchCon.grid(row=0, column=1, sticky="se", padx=15, pady=(15,5))

        tk.Label(searchCon, text="Search:", font=("Book Antiqua", 12), bg="#FFFFFF").pack(side="left")
        search_entry = tk.Entry(searchCon, font=("Book Antiqua", 12))
        search_entry.pack(side="left", ipadx=65, padx=5)

        # Keep reference of data
        self.all_data = [content for i in range(15)]  # sample dataset

        # Function to update table ----------------------------------------------------------------------
        def update_table(data):
            table.delete(*table.get_children())  # clear
            for row in data:
                table.insert('', 'end', values=row)

        update_table(self.all_data)

        # Search function
        def search():
            query = search_entry.get().lower()
            filtered = [row for row in self.all_data if query in str(row).lower()]
            update_table(filtered)

        tk.Button(searchCon, text="Go", command=search, font=("Book Antiqua", 10)).pack(side="left", padx=5)

        # Register Movie Button ==================================================================
        registerBtn = tk.Button(conBtn, bg="#CD4126", text="Register",
                                font=("Book Antiqua", 9), fg="#FFFFFF",
                                command=lambda: register_modal(self))
        registerBtn.grid(row=0, column=0, ipady=5, sticky="sw", ipadx=30, padx=25)
