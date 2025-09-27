import customtkinter as ctk
from Modals.Register import register_modal

class SalesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F4F4F4")

        # Main layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=1)

        # ================= Sidebar ================= #
        sidebar = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)

        logoLabel = ctk.CTkLabel(sidebar, text="🎬 Admin",
                                 font=("Book Antiqua", 18, "bold"),
                                 text_color="#CD4126")
        logoLabel.grid(row=0, column=0, sticky="nsew", pady=(30, 40))

        def menu_button(text, row, active=False, command=None):
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Book Antiqua", 13),
                fg_color="#EFE9E0" if active else "#FFFFFF",
                text_color="#665050",
                hover_color="#d6cfc5",
                corner_radius=6,
                command=command
            )
            btn.grid(row=row, column=0, sticky="ew", padx=15, pady=3, ipady=10)
            return btn

        menu_button("Movies", 2, command=lambda: controller.show_frame("AdminPage"))
        menu_button("Sales", 3, active=True, command=lambda: controller.show_frame("SalesPage"))
        menu_button("Sales History", 4, command=lambda: controller.show_frame("SalesHistoryPage"))

        logoutBtn = ctk.CTkButton(sidebar, text="Logout",
                                  font=("Book Antiqua", 12),
                                  fg_color="#CD4126", text_color="white",
                                  hover_color="#a8321d", corner_radius=6)
        logoutBtn.grid(row=6, column=0, sticky="sew", padx=15, pady=(10, 20), ipady=8)

        # ================= Main Content ================= #
        mainFrame = ctk.CTkFrame(self, fg_color="#F4F4F4")
        mainFrame.grid(row=0, column=1, sticky="nsew")
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)

        # ---- Title ---- #
        title = ctk.CTkLabel(mainFrame, text="Sales Management",
                             font=("Book Antiqua", 18, "bold"),
                             text_color="#665050")
        title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # ---- Table card ---- #
        tableCard = ctk.CTkFrame(mainFrame, fg_color="#FFFFFF", corner_radius=12)
        tableCard.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        tableCard.columnconfigure(tuple(range(6)), weight=1)  # 6 columns

        # Top bar inside table card
        cardTop = ctk.CTkFrame(tableCard, fg_color="#FFFFFF")
        cardTop.grid(row=0, column=0, columnspan=6, sticky="ew", padx=10, pady=(30,5))
        cardTop.columnconfigure(0, weight=1)
        cardTop.columnconfigure(1, weight=0)
        cardTop.columnconfigure(2, weight=0)

        search = ctk.CTkEntry(cardTop, placeholder_text="Search...",
                              font=("Book Antiqua", 12), width=250,
                              height=30 ,fg_color="#f4f4f4")
        search.grid(row=0, column=1, sticky="e", padx=10)

        addBtn = ctk.CTkButton(cardTop, text="Register",
                               font=("Book Antiqua", 12, "bold"),
                               fg_color="#CD4126", text_color="white",
                               hover_color="#a8321d", corner_radius=6,
                               height=30,
                               command=lambda: register_modal(self))
        addBtn.grid(row=0, column=2, sticky="e")

        # Table headers
        headers = ["ID", "Code", "Seat", "Price", "Genre", "Date"]
        self.headers = headers
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(tableCard,
                               text=h,
                               font=("Book Antiqua", 13, "bold"),
                               text_color="#665050", fg_color="#f9f7f4",
                               corner_radius=6, pady=8)
            lbl.grid(row=1, column=i, sticky="nsew", padx=5, pady=10)

        # Example data
        self.rows = [
            ("001", "PET001", "A1", "$300", "Horror", "Nov 5, 2025"),
            ("002", "PET002", "B3", "$250", "Animation", "Nov 5, 2025"),
            ("003", "PET003", "C5", "$400", "Action", "Nov 6, 2025"),
            ("004", "PET004", "D2", "$350", "Romance", "Nov 6, 2025"),
            ("005", "PET005", "E4", "$280", "Horror", "Nov 7, 2025"),
            ("006", "PET006", "F1", "$260", "Animation", "Nov 7, 2025"),
            ("007", "PET007", "G3", "$500", "Action", "Nov 8, 2025"),
            ("008", "PET008", "H5", "$330", "Drama", "Nov 8, 2025"),
            ("009", "PET009", "I2", "$450", "Sci-Fi", "Nov 9, 2025"),
            ("010", "PET010", "J4", "$320", "Thriller", "Nov 9, 2025"),
            ("011", "PET011", "K1", "$270", "Animation", "Nov 10, 2025"),
            ("012", "PET012", "L3", "$290", "Horror", "Nov 10, 2025"),
            ("013", "PET013", "M5", "$480", "Action", "Nov 11, 2025"),
            ("014", "PET014", "N2", "$310", "Romance", "Nov 11, 2025"),
            ("015", "PET015", "O4", "$500", "Crime", "Nov 12, 2025"),
            ("016", "PET016", "P1", "$260", "Animation", "Nov 12, 2025"),
            ("017", "PET017", "Q3", "$520", "Action", "Nov 13, 2025"),
            ("018", "PET018", "R5", "$300", "Romance", "Nov 13, 2025"),
            ("019", "PET019", "S2", "$280", "Horror", "Nov 14, 2025"),
            ("020", "PET020", "T4", "$490", "Action", "Nov 14, 2025"),
        ]

        self.page_size = 10
        self.current_page = 0
        self.tableCard = tableCard
        self.render_page()

        # ---- Pagination controls ---- #
        pagination = ctk.CTkFrame(mainFrame, fg_color="#F4F4F4")
        pagination.grid(row=2, column=0, sticky="ew", pady=(0, 60))

        prevBtn = ctk.CTkButton(pagination, text="◀ Previous",
                                fg_color="#FFFFFF", text_color="#665050",
                                hover_color="#d6cfc5", corner_radius=6,
                                width=100, command=self.prev_page)
        prevBtn.pack(side="left", padx=20)

        nextBtn = ctk.CTkButton(pagination, text="Next ▶",
                                fg_color="#FFFFFF", text_color="#665050",
                                hover_color="#d6cfc5", corner_radius=6,
                                width=100, command=self.next_page)
        nextBtn.pack(side="right", padx=20)

    # ================= Helper Methods ================= #
    def render_page(self):
        for widget in self.tableCard.winfo_children()[len(self.headers)+1:]:
            widget.destroy()

        start = self.current_page * self.page_size
        end = start + self.page_size
        for r, row in enumerate(self.rows[start:end], start=2):
            for c, val in enumerate(row):
                lbl = ctk.CTkLabel(self.tableCard,
                                   text=val,
                                   font=("Book Antiqua", 12),
                                   text_color="#333333")
                lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.rows):
            self.current_page += 1
            self.render_page()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page()
