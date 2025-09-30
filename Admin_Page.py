import customtkinter as ctk
from Modals.Register import register_modal


class AdminPage(ctk.CTkFrame):
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

        menu_button("Movies", 2, active=True, command=lambda: controller.show_frame("AdminPage"))
        menu_button("Sales", 3, command=lambda: controller.show_frame("SalesPage"))
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
        mainFrame.rowconfigure(1, weight=1)  # Table row grows

        # ---- Title ---- #
        title = ctk.CTkLabel(mainFrame, text="Movies Management",
                             font=("Book Antiqua", 18, "bold"),
                             text_color="#665050")
        title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # ---- Table card ---- #
        tableCard = ctk.CTkFrame(mainFrame, fg_color="#FFFFFF", corner_radius=12)
        tableCard.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        tableCard.columnconfigure(tuple(range(5)), weight=1)

        # Top bar inside table card
        cardTop = ctk.CTkFrame(tableCard, fg_color="#FFFFFF")
        cardTop.grid(row=0, column=0, columnspan=5, sticky="ew", padx=10, pady=(30,5))
        cardTop.columnconfigure(0, weight=1)
        cardTop.columnconfigure(1, weight=0)
        cardTop.columnconfigure(2, weight=0)

        search = ctk.CTkEntry(cardTop, placeholder_text="Search...",
                              font=("Book Antiqua", 12), width=250,
                              height=30 ,fg_color="#f4f4f4")
        search.grid(row=0, column=1, sticky="e", padx=10)

        addBtn = ctk.CTkButton(cardTop, text="Add New",
                               font=("Book Antiqua", 12, "bold"),
                               fg_color="#CD4126", text_color="white",
                               hover_color="#a8321d", corner_radius=6,
                               height=30,
                               command= lambda: register_modal(self, controller))
        addBtn.grid(row=0, column=2, sticky="e")

        # Table headers
        headers = ["ID", "Movie", "Genre", "Price", "Status"]
        self.headers = headers
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(tableCard,
                               text=h,
                               font=("Book Antiqua", 13, "bold"),
                               text_color="#665050", fg_color="#f9f7f4",
                               corner_radius=6,pady=8)
            lbl.grid(row=1, column=i, sticky="nsew", padx=5, pady=10)

        # Example data
        self.rows = [
            ("001", "Pet Sematary", "Horror", "$300", "Active"),
            ("002", "Frozen", "Animation", "$250", "Inactive"),
            ("003", "Avengers", "Action", "$400", "Active"),
            ("004", "Titanic", "Romance", "$350", "Inactive"),
            ("005", "The Conjuring", "Horror", "$280", "Active"),
            ("006", "Moana", "Animation", "$260", "Inactive"),
            ("007", "Inception", "Sci-Fi", "$500", "Active"),
            ("008", "Joker", "Drama", "$330", "Active"),
            ("009", "The Matrix", "Sci-Fi", "$450", "Active"),
            ("010", "Parasite", "Thriller", "$320", "Inactive"),
            ("011", "Lion King", "Animation", "$270", "Active"),
            ("012", "It", "Horror", "$290", "Inactive"),
            ("013", "Black Panther", "Action", "$480", "Active"),
            ("014", "La La Land", "Romance", "$310", "Inactive"),
            ("015", "The Godfather", "Crime", "$500", "Active"),
            ("016", "Coco", "Animation", "$260", "Active"),
            ("017", "Avengers: Endgame", "Action", "$520", "Active"),
            ("018", "The Notebook", "Romance", "$300", "Inactive"),
            ("019", "Get Out", "Horror", "$280", "Active"),
            ("020", "Spider-Man: No Way Home", "Action", "$490", "Active"),
        ]

        # Pagination setup
        self.page_size = 10
        self.current_page = 0
        self.tableCard = tableCard
        self.render_page()

        # ---- Pagination controls ---- #
        pagination = ctk.CTkFrame(mainFrame, fg_color="#F4F4F4")
        pagination.grid(row=2, column=0, sticky="ew", pady=(0, 60))

        prevBtn = ctk.CTkButton(
            pagination,
            text="◀ Previous",
            fg_color="#FFFFFF",
            text_color="#665050",
            hover_color="#d6cfc5",
            corner_radius=6,
            width=100,
            command=self.prev_page
        )
        prevBtn.pack(side="left", padx=20)

        nextBtn = ctk.CTkButton(
            pagination,
            text="Next ▶",
            fg_color="#FFFFFF",
            text_color="#665050",
            hover_color="#d6cfc5",
            corner_radius=6,
            width=100,
            command=self.next_page
        )
        nextBtn.pack(side="right", padx=20)

    # ================= Helper Methods ================= #
    def status_badge(self, parent, text):
        color_map = {
            "Active": "#22c55e",
            "Inactive": "#ef4444",
            "Pending": "#f59e0b",
        }
        return ctk.CTkLabel(
            parent,
            text=text,
            font=("Book Antiqua", 13, "bold"),
            text_color="white",
            fg_color=color_map.get(text, "#6b7280"),
            corner_radius=8,
            padx=10,
            pady=4
        )

    def render_page(self):
        # Clear old rows (everything below header row)
        for widget in self.tableCard.winfo_children()[len(self.headers) + 1:]:
            widget.destroy()

        start = self.current_page * self.page_size
        end = start + self.page_size
        for r, row in enumerate(self.rows[start:end], start=2):
            for c, val in enumerate(row):
                if self.headers[c] == "Status":
                    badge = self.status_badge(self.tableCard, val)
                    badge.grid(row=r, column=c, sticky="nsew", padx=10, pady=8)
                else:
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
