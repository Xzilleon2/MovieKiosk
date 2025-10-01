import customtkinter as ctk
from tkinter import filedialog, messagebox


def register_modal(self, controller):
    """
    Modal window for registering a new movie.
    :param self: parent frame
    :param controller: Controller instance (handles saving/logic)
    """
    modal = ctk.CTkToplevel(self)
    modal.title("Register Movie")
    modal.configure(fg_color="#F4F4F4")
    modal.transient(self)
    modal.grab_set()

    # Modal size & center
    w, h = 480, 700
    parent_x = self.winfo_rootx()
    parent_y = self.winfo_rooty()
    parent_w = self.winfo_width()
    parent_h = self.winfo_height()
    x = parent_x + (parent_w // 2) - (w // 2)
    y = parent_y + (parent_h // 2) - (h // 2) - 15
    modal.geometry(f"{w}x{h}+{x}+{y}")

    # ====== CARD CONTAINER ====== #
    card = ctk.CTkFrame(modal, fg_color="#FFFFFF", corner_radius=12)
    card.pack(expand=True, fill="both", padx=20, pady=20)

    card.grid_rowconfigure(0, weight=1)
    card.grid_rowconfigure(1, weight=0)
    card.grid_columnconfigure(0, weight=1)

    content = ctk.CTkFrame(card, fg_color="#FFFFFF")
    content.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

    # ===== Title Label =====
    ctk.CTkLabel(
        content, text="🎬 Register New Movie",
        font=("Book Antiqua", 22, "bold"),
        text_color="#CD4126"
    ).pack(pady=(10, 20))

    # ===== Styles =====
    entry_style = {
        "font": ("Book Antiqua", 12),
        "fg_color": "#f9f9f9",
        "text_color": "black",
        "border_color": "#d6cfc5",
        "corner_radius": 6
    }
    combo_style = {
        "fg_color": "#f9f9f9",
        "text_color": "black",
        "button_color": "#CD4126",
        "button_hover_color": "#a8321d",
        "border_color": "#d6cfc5",
        "corner_radius": 6
    }

    # ===== Helpers =====
    def labeled_entry(label, parent, **kwargs):
        ctk.CTkLabel(parent, text=label, text_color="#665050", anchor="w").pack(fill="x", padx=15)
        entry = ctk.CTkEntry(parent, **kwargs)
        entry.pack(fill="x", padx=15, pady=5)
        return entry

    def labeled_combo(label, parent, values, **kwargs):
        ctk.CTkLabel(parent, text=label, text_color="#665050", anchor="w").pack(fill="x", padx=15)
        combo = ctk.CTkComboBox(parent, values=values, **kwargs)
        combo.pack(fill="x", padx=15, pady=5)
        return combo

    # ===== Inputs =====
    title_entry = labeled_entry("Title", content, **entry_style)
    genre_combobox = labeled_combo("Genre", content,
                                   ["Action", "Horror", "Comedy", "Drama", "Sci-Fi", "Romance"], **combo_style)
    price_entry = labeled_entry("Price", content, **entry_style)
    duration_entry = labeled_entry("Duration (mins)", content, **entry_style)
    rating_combobox = labeled_combo("Rating", content,
                                    ["G", "PG", "PG-13", "R", "NC-17"], **combo_style)
    status_combobox = labeled_combo("Status", content,
                                    ["Available", "NotAvailable"], **combo_style)

    # ===== Description =====
    ctk.CTkLabel(content, text="Description", text_color="#665050", anchor="w").pack(fill="x", padx=15, pady=(10, 0))
    description_text = ctk.CTkTextbox(
        content, height=160, fg_color="#f9f9f9", text_color="black",
        border_color="#d6cfc5", corner_radius=6, wrap="word"
    )
    description_text.pack(fill="x", padx=15, pady=5)
    description_text.configure(padx=8, pady=8)

    # ===== Poster Upload =====
    def upload_poster():
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file:
            poster_path_entry.delete(0, "end")
            poster_path_entry.insert(0, file)

    ctk.CTkLabel(content, text="Poster", text_color="#665050", anchor="w").pack(fill="x", padx=15, pady=(10, 0))
    poster_frame = ctk.CTkFrame(content, fg_color="#f9f9f9", corner_radius=8)
    poster_frame.pack(fill="x", padx=15, pady=5)
    poster_frame.columnconfigure(0, weight=1)

    poster_path_entry = ctk.CTkEntry(poster_frame, **entry_style)
    poster_path_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    upload_btn = ctk.CTkButton(
        poster_frame, text="Browse", fg_color="#CD4126", hover_color="#a8321d",
        text_color="white", width=80, command=upload_poster
    )
    upload_btn.grid(row=0, column=1, padx=5)

    # ===== Register Button =====
    def on_register():
        movie_data = {
            "title": title_entry.get().strip(),
            "genre": genre_combobox.get().strip(),
            "price": price_entry.get().strip(),
            "duration": duration_entry.get().strip(),
            "rating": rating_combobox.get().strip(),
            "status": status_combobox.get().strip(),
            "description": description_text.get("1.0", "end-1c").strip(),
            "poster": poster_path_entry.get().strip()
        }

        # --- Validation ---
        if not movie_data["title"]:
            messagebox.showerror("Validation Error", "Title is required.")
            return
        if not movie_data["genre"]:
            messagebox.showerror("Validation Error", "Genre is required.")
            return

        # Call controller
        ok, msg = controller.save(movie_data)
        if ok:
            messagebox.showinfo("Success", msg if msg else "Movie registered successfully!")
            modal.destroy()
        else:
            messagebox.showerror("Error", msg if msg else "Failed to register movie.")

    register_btn = ctk.CTkButton(
        card, text="➕ Register Movie",
        font=("Book Antiqua", 14, "bold"),
        fg_color="#CD4126", hover_color="#a8321d",
        text_color="white", corner_radius=8, height=40,
        command=on_register
    )
    register_btn.grid(row=1, column=0, pady=15, ipadx=20, ipady=5)
