import customtkinter as ctk
from Classes.MoviesCntrl_Class import MoviesCntrl
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os, shutil


def register_modal(self, controller):
    modal = ctk.CTkToplevel(self)
    modal.title("Add New Movie")
    modal.configure(fg_color="#F4F4F4")
    modal.transient(self)
    modal.grab_set()

    # Modal size & center
    w, h = 500, 720
    parent_x = self.winfo_rootx()
    parent_y = self.winfo_rooty()
    parent_w = self.winfo_width()
    parent_h = self.winfo_height()
    x = parent_x + (parent_w // 2) - (w // 2)
    y = parent_y + (parent_h // 2) - (h // 2) - 15
    modal.geometry(f"{w}x{h}+{x}+{y}")

    # ====== CARD CONTAINER ====== #
    card = ctk.CTkFrame(modal, fg_color="#FFFFFF", corner_radius=12)
    card.pack(expand=True, fill="both", padx=16, pady=16)

    card.grid_rowconfigure(0, weight=1)
    card.grid_rowconfigure(1, weight=0)
    card.grid_columnconfigure(0, weight=1)

    content = ctk.CTkFrame(card, fg_color="#FFFFFF")
    content.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

    # ===== Styles =====
    entry_style = {
        "font": ("Book Antiqua", 12),
        "fg_color": "#FAFAFA",
        "text_color": "#222",
        "border_color": "#E0E0E0",
        "corner_radius": 6,
        "height": 32
    }
    combo_style = {
        "fg_color": "#FAFAFA",
        "text_color": "#222",
        "button_color": "#CD4126",
        "button_hover_color": "#a8321d",
        "border_color": "#E0E0E0",
        "corner_radius": 6,
        "height": 32
    }

    # ===== Poster Upload with Preview (TOP) =====
    poster_frame = ctk.CTkFrame(content, fg_color="white")
    poster_frame.pack(fill="x", padx=12, pady=6)

    # Preview (centered)
    poster_preview = ctk.CTkLabel(
        poster_frame, text="No Poster Selected",
        text_color="#888", width=180, height=200, anchor="center"
    )
    poster_preview.pack(side="left", padx=6, pady=6)

    assets_dir = os.path.join(os.getcwd(), "Assets", "Posters")
    os.makedirs(assets_dir, exist_ok=True)
    poster_filename = {"value": None}

    def upload_poster():
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file:
            fname = os.path.basename(file)
            dest = os.path.join(assets_dir, fname)
            shutil.copy(file, dest)  # save in Assets/Posters
            poster_filename["value"] = fname

            # preview
            img = Image.open(file)
            img.thumbnail((180, 220))
            tk_img = ImageTk.PhotoImage(img)
            poster_preview.configure(image=tk_img, text="")
            poster_preview.image = tk_img  # keep reference

    # Upload Button (right side)
    upload_btn = ctk.CTkButton(
        poster_frame, text="Upload Poster",
        fg_color="#CD4126", hover_color="#a8321d",
        text_color="white", corner_radius=6, height=34,
        command=upload_poster
    )
    upload_btn.pack(side="left", padx=6, pady=6)

    # ===== Title =====
    ctk.CTkLabel(content, text="Title", text_color="#555", anchor="w").pack(fill="x", padx=12, pady=(6, 0))
    title_entry = ctk.CTkEntry(content, **entry_style)
    title_entry.pack(fill="x", padx=12, pady=4)

    # ===== Row 1: Genre + Price =====
    row1 = ctk.CTkFrame(content, fg_color="white")
    row1.pack(fill="x", padx=12, pady=6)
    row1.grid_columnconfigure((0, 1), weight=1)

    duration_label = ctk.CTkLabel(row1, text="Duration (mins)", text_color="#555", anchor="w")
    duration_label.grid(row=0, column=0, sticky="w", padx=2)
    duration_entry = ctk.CTkEntry(row1, **entry_style, width=100)
    duration_entry.grid(row=1, column=0, padx=2, pady=4)

    price_label = ctk.CTkLabel(row1, text="Price", text_color="#555", anchor="w")
    price_label.grid(row=0, column=1, sticky="w", padx=2)
    price_entry = ctk.CTkEntry(row1, **entry_style, width=120)
    price_entry.grid(row=1, column=1, padx=2, pady=4)

    # ===== Row 2: Duration + Rating + Status =====
    row2 = ctk.CTkFrame(content, fg_color="white")
    row2.pack(fill="x", padx=12, pady=6)
    row2.grid_columnconfigure((0, 1, 2), weight=1)

    genre_label = ctk.CTkLabel(row2, text="Genre", text_color="#555", anchor="w")
    genre_label.grid(row=0, column=0, sticky="w", padx=2)
    genre_combobox = ctk.CTkComboBox(
        row2,
        values=[
            "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
            "Documentary", "Drama", "Family", "Fantasy", "History", "Horror",
            "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short",
            "Sport", "Superhero", "Thriller", "War", "Western"
        ],
        **combo_style,
        width=160
    )
    genre_combobox.grid(row=1, column=0, padx=2, pady=4)

    rating_label = ctk.CTkLabel(row2, text="Rating", text_color="#555", anchor="w")
    rating_label.grid(row=0, column=1, sticky="w", padx=2)
    rating_combobox = ctk.CTkComboBox(
        row2, values=["G", "PG", "PG-13", "R", "NC-17"],
        **combo_style, width=100
    )
    rating_combobox.grid(row=1, column=1, padx=2, pady=4)

    status_label = ctk.CTkLabel(row2, text="Status", text_color="#555", anchor="w")
    status_label.grid(row=0, column=2, sticky="w", padx=2)
    status_combobox = ctk.CTkComboBox(
        row2, values=["Available", "NotAvailable"],
        **combo_style, width=120
    )
    status_combobox.grid(row=1, column=2, padx=2, pady=4)

    # ===== Description =====
    ctk.CTkLabel(content, text="Description", text_color="#555", anchor="w").pack(fill="x", padx=12, pady=(6, 0))
    description_text = ctk.CTkTextbox(
        content, height=150, fg_color="#FAFAFA", text_color="#222",
        border_color="#E0E0E0", corner_radius=6, wrap="word"
    )
    description_text.pack(fill="both", expand=True, padx=12, pady=4)
    description_text.configure(padx=6, pady=6)

    # ===== Register Button =====
    def on_register():
        title = title_entry.get().strip()
        genre = genre_combobox.get().strip()
        price = price_entry.get().strip()
        duration = duration_entry.get().strip()
        rating = rating_combobox.get().strip()
        description = description_text.get("1.0", "end-1c").strip()
        poster = poster_filename["value"]
        status = status_combobox.get().strip()

        Cntrl = MoviesCntrl(title, genre, price, duration, rating, description, poster, status)
        ok = Cntrl.AddMovie()

        if ok:
            messagebox.showinfo("Success", "Movie added successfully!")
        else:
            messagebox.showerror("Error", "Failed to add movie.")

        modal.destroy()

    register_btn = ctk.CTkButton(
        card, text="➕ Register Movie",
        font=("Book Antiqua", 13, "bold"),
        fg_color="#CD4126", hover_color="#a8321d",
        text_color="white", corner_radius=6, height=38,
        command=on_register
    )
    register_btn.grid(row=1, column=0, pady=12, ipadx=12, ipady=2)

    modal.wait_window()
