import tkinter as tk
from tkinter import ttk, PhotoImage
import os
from Modals.Register import register_modal

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F4F4")

        #Main layout for admin page
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=1)

        # Side frame for column 1 ============================================================
        sideMenu = tk.Frame(self, bg="#F4F4F4")
        sideMenu.grid(row=0, column=0, sticky="nsew")
        sideMenu.rowconfigure(0, weight=1)
        sideMenu.columnconfigure(0, weight=1)

        #Frame Content for side Menu
        sideMenuCon = tk.Frame(sideMenu, bg="#FFFFFF", relief="groove")
        sideMenuCon.grid(row=0, column=0, sticky="nsew", padx=(25, 5), pady=55)
        sideMenuCon.columnconfigure(0, weight=1)

        #Image path
        img_path = os.path.join(os.path.dirname(__file__), "Assets", "Bag.png")
        self.iconIMG = PhotoImage(file=img_path)

        # IMG LABEL
        imgLabel = tk.Label(sideMenuCon, bg="#FFFFFF", image=self.iconIMG)
        imgLabel.grid(row=0, column=0, sticky="nsew", ipady=30)

        # Buttons for tables
        movieBtn = tk.Button(sideMenuCon, bg="#EFE9E0", text="Movies",
                             font=("Book Antiqua", 16), fg="#665050", relief="flat")
        movieBtn.grid(row=1, column=0, sticky="nsew", ipady=30)

        salesBtn = tk.Button(sideMenuCon, bg="#FFFFFF", text="Sales",
                             font=("Book Antiqua", 16), fg="#665050", relief="flat")
        salesBtn.grid(row=2, column=0, sticky="nsew", ipady=30)

        salesHistoryBtn = tk.Button(sideMenuCon, bg="#FFFFFF", text="Sales History",
                                    font=("Book Antiqua", 16), fg="#665050", relief="flat")
        salesHistoryBtn.grid(row=3, column=0, sticky="nsew", ipady=30)

        logoutBtn = tk.Button(sideMenuCon, bg="#FFFFFF", text="Logout",
                              font=("Book Antiqua", 16), fg="#665050", relief="flat")
        logoutBtn.grid(row=4, column=0, sticky="nsew", ipady=30)

        # Main frame for tables ============================================================
        mainMenu = tk.Frame(self, bg="#F4F4F4")
        mainMenu.grid(row=0, column=1, sticky="nsew")
        mainMenu.rowconfigure(0, weight=1)
        mainMenu.columnconfigure(0, weight=1)

        # Frame container for tables
        mainMenuCon = tk.Frame(mainMenu, bg="#FFFFFF", relief="groove")
        mainMenuCon.grid(row=0, column=0, sticky="nsew", padx=(5, 25), pady=55)
        mainMenuCon.rowconfigure(0, weight=0)
        mainMenuCon.rowconfigure(1, weight=1)
        mainMenuCon.rowconfigure(2, weight=0)
        mainMenuCon.columnconfigure(0, weight=1)

        # Title Row =====================================================================
        Title = tk.Label(mainMenuCon, bg="#FFFFFF", text="MOVIE TICKETING ADMIN",
                         font=("Book Antiqua", 30), fg="#665050", anchor="w")
        Title.grid(row=0, column=0, sticky="nsew", ipady=30, padx=20)

        # Container for Table =====================================================================
        tableCon = tk.Frame(mainMenuCon, bg="#FFFFFF")
        tableCon.grid(row=1, column=0, sticky="nsew", pady=10)

        # Table Sample Data
        content = ['001', 'Pet Sematary', 'visiting their old house in...', '$300',
                   'Horror|Thriller', 'November 5, 2025']

        # Style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Book Antiqua", 18, "bold"),
                        foreground="#665050", padding=10)
        style.configure("Treeview", font=("Book Antiqua", 12),
                        foreground="#665050", rowheight=40)

        # Table
        table = ttk.Treeview(tableCon,
                             columns=('ID', 'TITLE', 'Description', 'Price', 'Genre', 'Date'),
                             show='headings')
        for col in ('ID', 'TITLE', 'Description', 'Price', 'Genre', 'Date'):
            table.heading(col, text=col, anchor='center')
        table.pack(expand=True, fill="both", padx=20)

        # Columns (data alignment)
        table.column('ID', anchor='e', width=80)  # Right align numbers
        table.column('TITLE', anchor='w', width=200)  # Left align text
        table.column('Description', anchor='w', width=300, stretch=False)
        table.column('Price', anchor='e', width=100)  # Right align price
        table.column('Genre', anchor='w', width=150)
        table.column('Date', anchor='w', width=150)

        # Random content
        for i in range(15):
            table.insert(parent='', index=0, values=content)

        # --- Search Bar ---
        searchCon = tk.Frame(mainMenuCon, bg="#FFFFFF")
        searchCon.grid(row=0, column=0, sticky="se", padx=15, pady=5)

        tk.Label(searchCon, text="Search:", font=("Book Antiqua", 12), bg="#FFFFFF").pack(side="left")
        search_entry = tk.Entry(searchCon, font=("Book Antiqua", 12))
        search_entry.pack(side="left", ipadx=65, padx=5)

        # Keep reference of data
        self.all_data = [content for i in range(15)]  # sample dataset

        # Function to update table
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

        # --- Sorting function ---
        def sort(col, reverse):
            data = [(table.set(k, col), k) for k in table.get_children('')]
            data.sort(reverse=reverse)

            for index, (val, k) in enumerate(data):
                table.move(k, '', index)

            # Toggle sort order
            table.heading(col, command=lambda: sort(col, not reverse))

        # Disable resizing of columns
        def handle_event(event):
            if table.identify_region(event.x, event.y) == "separator":
                return "break"  # prevent dragging the separator

        table.bind("<Button-1>", handle_event)

        # Add sorting to each heading
        for col in ('ID', 'TITLE', 'Description', 'Price', 'Genre', 'Date'):
            table.heading(col, text=col, anchor='center', command=lambda c=col: sort(c, False))

        # Container for Buttons ================================================================
        conBtn = tk.Frame(mainMenuCon, bg="#FFFFFF")
        conBtn.grid(row=2, column=0, sticky="nsew", ipady=50)

        # Register Movie Button
        registerBtn = tk.Button(conBtn, bg="#CD4126", text="Register",
                                font=("Book Antiqua", 14), fg="#FFFFFF",
                                command=lambda: register_modal(self))  # <-- call modal
        registerBtn.pack(side=tk.RIGHT, anchor=tk.NE, ipady=10, ipadx=50, padx=20)