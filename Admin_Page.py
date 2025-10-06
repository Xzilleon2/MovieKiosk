import customtkinter as ctk
from Modals.Register import register_modal
from Classes.MoviesView_Class import MoviesView
from Modals.Delete import delete_modal
from Modals.Update import update_modal

class AdminPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#E8FFD7")

        # Main layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=1)

        # ================= Sidebar ================= #
        sidebar = ctk.CTkFrame(self, fg_color="#93DA97", corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)

        logoLabel = ctk.CTkLabel(sidebar, text="🎬 Admin",
                                 font=("Book Antiqua", 18, "bold"),
                                 text_color="#3E5F44")
        logoLabel.grid(row=0, column=0, sticky="nsew", pady=(30, 40))

        def menu_button(text, row, active=False, command=None):
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Book Antiqua", 13),
                fg_color="#5E936C" if active else "#93DA97",
                text_color="#3E5F44",
                hover_color="#E8FFD7",
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
                                  fg_color="#3E5F44", text_color="#E8FFD7",
                                  hover_color="#5E936C", corner_radius=6,
                                  command= lambda: controller.show_frame("HomePage"))
        logoutBtn.grid(row=6, column=0, sticky="sew", padx=15, pady=(10, 20), ipady=8)

        # ================= Main Content ================= #
        mainFrame = ctk.CTkFrame(self, fg_color="#E8FFD7")
        mainFrame.grid(row=0, column=1, sticky="nsew")
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)  # Table row grows

        # ---- Title ---- #
        title = ctk.CTkLabel(mainFrame, text="Movies Management",
                             font=("Book Antiqua", 18, "bold"),
                             text_color="#3E5F44")
        title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # ---- Table card ---- #
        tableCard = ctk.CTkFrame(mainFrame, fg_color="#93DA97", corner_radius=12)
        tableCard.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        tableCard.columnconfigure(tuple(range(8)), weight=1)

        # Top bar inside table card
        cardTop = ctk.CTkFrame(tableCard, fg_color="#93DA97")
        cardTop.grid(row=0, column=0, columnspan=10, sticky="ew", padx=10, pady=(30, 5))
        cardTop.columnconfigure(0, weight=1)
        cardTop.columnconfigure(1, weight=0)
        cardTop.columnconfigure(2, weight=0)

        self.search_entry = ctk.CTkEntry(cardTop, placeholder_text="Search...",
                                         font=("Book Antiqua", 12), width=250,
                                         height=30, fg_color="#E8FFD7", text_color="#3E5F44")
        self.search_entry.grid(row=0, column=1, sticky="e", padx=10)
        self.search_entry.bind("<KeyRelease>", self.handle_search)  # Bind search event

        addBtn = ctk.CTkButton(cardTop, text="Add New",
                               font=("Book Antiqua", 12, "bold"),
                               fg_color="#3E5F44", text_color="#E8FFD7",
                               hover_color="#5E936C", corner_radius=6,
                               height=30,
                               command=lambda: register_modal(self))
        addBtn.grid(row=0, column=2, sticky="e")

        # Table headers
        headers = ["ID", "Movie", "Genre", "Price", "Duration", "Rating", "Status", "Action"]
        self.headers = headers
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(tableCard,
                               text=h,
                               font=("Book Antiqua", 13, "bold"),
                               text_color="#3E5F44", fg_color="#E8FFD7",
                               corner_radius=6, pady=8)
            lbl.grid(row=1, column=i, sticky="nsew", padx=5, pady=10)

        # Pagination setup
        self.page_size = 10
        self.current_page = 0
        self.tableCard = tableCard
        self.all_movies = MoviesView().getMoviesThisMonth()  # Fetch movies once during init
        self.filtered_movies = self.all_movies  # Initialize with all movies
        self.render_page()

        # ---- Pagination controls ---- #
        pagination = ctk.CTkFrame(mainFrame, fg_color="#E8FFD7")
        pagination.grid(row=2, column=0, sticky="ew", pady=(0, 60))

        prevBtn = ctk.CTkButton(
            pagination,
            text="◀ Previous",
            fg_color="#93DA97",
            text_color="#3E5F44",
            hover_color="#5E936C",
            corner_radius=6,
            width=100,
            command=self.prev_page
        )
        prevBtn.pack(side="left", padx=20)

        nextBtn = ctk.CTkButton(
            pagination,
            text="Next ▶",
            fg_color="#93DA97",
            text_color="#3E5F44",
            hover_color="#5E936C",
            corner_radius=6,
            width=100,
            command=self.next_page
        )
        nextBtn.pack(side="right", padx=20)

    # ================= Helper Methods ================= #
    def status_badge(self, parent, text):
        color_map = {
            "Available": "#22c55e",
            "NotAvailable": "#ef4444",
        }
        return ctk.CTkLabel(
            parent,
            text=text,
            font=("Book Antiqua", 13, "bold"),
            text_color="#E8FFD7",
            fg_color=color_map.get(text, "#6b7280"),
            corner_radius=8,
            padx=10,
            pady=4
        )

    def handle_search(self, event=None):
        """Handle search input and filter movies."""
        query = self.search_entry.get().strip().lower()
        if query:
            # Filter movies based on title or genre
            self.filtered_movies = [
                movie for movie in self.all_movies
                if query in movie["title"].lower() or query in movie["genre"].lower()
            ]
        else:
            # If search is empty, show all movies
            self.filtered_movies = self.all_movies

        self.current_page = 0  # Reset to first page on search
        self.render_page()

    def render_page(self):
        """Render the current page of movies (filtered or all)."""
        # Clear old rows
        for widget in self.tableCard.winfo_children()[len(self.headers) + 1:]:
            widget.destroy()

        # Use filtered movies if available, else use all movies
        self.rows = self.filtered_movies if self.filtered_movies else None

        # Display message if no movies are found
        if not self.rows:
            lbl = ctk.CTkLabel(self.tableCard, text="No movies found",
                               font=("Book Antiqua", 12), text_color="#3E5F44")
            lbl.grid(row=2, column=0, columnspan=len(self.headers), pady=20)
            return

        start = self.current_page * self.page_size
        end = start + self.page_size

        for r, movie in enumerate(self.rows[start:end], start=2):
            for c, header in enumerate(self.headers):
                if header == "ID":
                    lbl = ctk.CTkLabel(self.tableCard, text=str(movie["id"]),
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Movie":
                    lbl = ctk.CTkLabel(self.tableCard, text=movie["title"],
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Genre":
                    lbl = ctk.CTkLabel(self.tableCard, text=movie["genre"],
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Price":
                    price_text = f"₱{movie['price']:.2f}"
                    lbl = ctk.CTkLabel(self.tableCard, text=price_text,
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Duration":
                    duration_text = f"{movie['duration']} mins" if isinstance(movie['duration'], int) else "Invalid Duration"
                    lbl = ctk.CTkLabel(self.tableCard, text=duration_text,
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Rating":
                    lbl = ctk.CTkLabel(self.tableCard, text=movie["rating"],
                                       font=("Book Antiqua", 12), text_color="#3E5F44")
                    lbl.grid(row=r, column=c, sticky="nsew", padx=10, ipady=10)

                elif header == "Status":
                    badge = self.status_badge(self.tableCard, movie["status"])
                    badge.grid(row=r, column=c, sticky="nsew", padx=10, pady=8)

                elif header == "Action":
                    action_frame = ctk.CTkFrame(self.tableCard, fg_color="#93DA97")
                    action_frame.grid(row=r, column=c, sticky="nsew", padx=5, pady=8)
                    action_frame.columnconfigure((0, 1), weight=1)

                    # Delete Button
                    del_btn = ctk.CTkButton(
                        action_frame, text="🗑", width=30, height=30,
                        fg_color="#ef4444", hover_color="#dc2626",
                        command=lambda m_id=movie["id"], m_title=movie["title"]: delete_modal(self, m_id, m_title)
                    )
                    del_btn.grid(row=0, column=0, padx=2, sticky="nsew")

                    # Update Button
                    upd_btn = ctk.CTkButton(
                        action_frame, text="🖋", width=30, height=30,
                        fg_color="#22c55e", hover_color="#16a34a",
                        command=lambda m_id=movie["id"], m_title=movie["title"], m_genre=movie["genre"],
                                       m_price=movie["price"], m_duration=movie["duration"], m_rating=movie["rating"],
                                       m_status=movie["status"], m_description=movie["description"], m_poster=movie["poster"]:
                        update_modal(self, m_id, m_title, m_genre, m_price, m_duration, m_rating, m_status, m_description, m_poster)
                    )
                    upd_btn.grid(row=0, column=1, padx=2, sticky="nsew")

    def next_page(self):
        """Go to the next page of movies."""
        if (self.current_page + 1) * self.page_size < len(self.rows):
            self.current_page += 1
            self.render_page()

    def prev_page(self):
        """Go to the previous page of movies."""
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page()

    def refresh_movies(self):
        try:
            self.all_movies = MoviesView().getMoviesThisMonth() or []
            self.filtered_movies = self.all_movies
            self.current_page = 0
            self.render_page()
        except Exception as e:
            lbl = ctk.CTkLabel(self.tableCard, text=f"Error loading movies: {str(e)}",
                               font=("Book Antiqua", 12), text_color="#ef4444")
            lbl.grid(row=2, column=0, columnspan=len(self.headers), pady=20)