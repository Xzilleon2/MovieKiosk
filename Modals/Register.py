import customtkinter as ctk
from Classes.MoviesCntrl_Class import MoviesCntrl
from tkinter import filedialog, messagebox
from PIL import Image
import os
import shutil
from datetime import datetime

class HiddenScrollbarFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Hide scrollbar by setting its width to 0
        self._scrollbar.configure(width=0)

def register_modal(self):
    modal = ctk.CTkToplevel(self)
    modal.title("Register New Movie")
    modal.configure(fg_color="#E8FFD7")
    modal.transient(self)
    modal.grab_set()

    w, h = 520, 760
    parent_x = self.winfo_rootx()
    parent_y = self.winfo_rooty()
    parent_w = self.winfo_width()
    parent_h = self.winfo_height()
    x = parent_x + (parent_w // 2) - (w // 2)
    y = parent_y + (parent_h // 2) - (h // 2) - 15
    modal.geometry(f"{w}x{h}+{x}+{y}")

    card = ctk.CTkFrame(modal, fg_color="#93DA97", corner_radius=12)
    card.pack(expand=True, fill="both", padx=15, pady=15)
    card.grid_rowconfigure(0, weight=1)
    card.grid_rowconfigure(1, weight=0)
    card.grid_columnconfigure(0, weight=1)

    # Use HiddenScrollbarFrame instead of CTkFrame
    content = HiddenScrollbarFrame(card, fg_color="#93DA97", scrollbar_button_color="#93DA97")
    content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    label_style = {"font": ("Book Antiqua", 12), "text_color": "#3E5F44", "anchor": "w"}
    entry_style = {"font": ("Book Antiqua", 12), "fg_color": "#E8FFD7", "text_color": "#3E5F44",
                   "border_color": "#5E936C", "corner_radius": 6, "height": 34}
    combo_style = {"font": ("Book Antiqua", 12), "fg_color": "#E8FFD7", "text_color": "#3E5F44",
                   "button_color": "#3E5F44", "button_hover_color": "#5E936C", "border_color": "#5E936C",
                   "corner_radius": 6, "height": 34}
    button_style = {"font": ("Book Antiqua", 13, "bold"), "fg_color": "#3E5F44", "hover_color": "#5E936C",
                    "text_color": "#E8FFD7", "corner_radius": 6, "height": 38}

    poster_frame = ctk.CTkFrame(content, fg_color="#93DA97")
    poster_frame.pack(fill="x", padx=10, pady=5)
    poster_preview = ctk.CTkLabel(poster_frame, text="No Poster Selected", font=("Book Antiqua", 12),
                                  text_color="#3E5F44", width=130, height=150, anchor="center",
                                  fg_color="#E8FFD7", corner_radius=6)
    poster_preview.pack(pady=5)

    assets_dir = os.path.join(os.path.dirname(__file__), "Assets", "Posters")
    os.makedirs(assets_dir, exist_ok=True)
    poster_filename = {"value": ""}

    def upload_poster():
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file:
            fname = os.path.basename(file)
            dest = os.path.join(assets_dir, fname)
            try:
                shutil.copy(file, dest)
                poster_filename["value"] = fname
                img = Image.open(dest).thumbnail((180, 200))
                ctk_img = ctk.CTkImage(light_image=Image.open(dest), size=(180, 200))
                poster_preview.configure(image=ctk_img, text="")
                poster_preview.image = ctk_img
            except Exception as e:
                print(f"Error loading uploaded poster: {e}")
                poster_preview.configure(text="Error loading poster")

    upload_btn = ctk.CTkButton(poster_frame, text="Upload Poster", command=upload_poster, **button_style)
    upload_btn.pack(pady=5)

    ctk.CTkLabel(content, text="Title", **label_style).pack(fill="x", padx=10, pady=(10, 0))
    title_entry = ctk.CTkEntry(content, **entry_style)
    title_entry.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(content, text="Release Date (YYYY-MM-DD)", **label_style).pack(fill="x", padx=10, pady=(10, 0))
    release_date_entry = ctk.CTkEntry(content, **entry_style, placeholder_text="e.g., 2025-10-01")
    release_date_entry.pack(fill="x", padx=10, pady=5)
    release_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    row1 = ctk.CTkFrame(content, fg_color="#93DA97")
    row1.pack(fill="x", padx=10, pady=5)
    row1.grid_columnconfigure((0, 1), weight=1)

    duration_label = ctk.CTkLabel(row1, text="Duration (mins)", **label_style)
    duration_label.grid(row=0, column=0, sticky="w", padx=5, pady=(0, 2))
    duration_entry = ctk.CTkEntry(row1, **entry_style, width=220)
    duration_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    price_label = ctk.CTkLabel(row1, text="Price", **label_style)
    price_label.grid(row=0, column=1, sticky="w", padx=5, pady=(0, 2))
    price_entry = ctk.CTkEntry(row1, **entry_style, width=220)
    price_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    row2 = ctk.CTkFrame(content, fg_color="#93DA97")
    row2.pack(fill="x", padx=10, pady=5)
    row2.grid_columnconfigure((0, 1, 2, 3), weight=1)

    genre_label = ctk.CTkLabel(row2, text="Genre", **label_style)
    genre_label.grid(row=0, column=0, sticky="w", padx=5, pady=(0, 2))
    genre_combobox = ctk.CTkComboBox(row2, values=["Action | Adventure", "Animation | Biography", "Comedy | Crime",
                                                  "Documentary | Drama", "Family | Fantasy", "History | Horror",
                                                  "Music | Musical", "Mystery | Romance", "Sci-Fi | Short",
                                                  "Sport | Superhero", "Thriller | War", "Western"],
                                     **combo_style, width=150)
    genre_combobox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    genre_combobox.set("Action | Adventure")

    rating_label = ctk.CTkLabel(row2, text="Rating", **label_style)
    rating_label.grid(row=0, column=1, sticky="w", padx=5, pady=(0, 2))
    rating_combobox = ctk.CTkComboBox(row2, values=["G", "PG", "PG-13", "R", "NC-17"], **combo_style, width=150)
    rating_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    rating_combobox.set("PG")

    status_label = ctk.CTkLabel(row2, text="Status", **label_style)
    status_label.grid(row=0, column=2, sticky="w", padx=5, pady=(0, 2))
    status_combobox = ctk.CTkComboBox(row2, values=["Available", "NotAvailable"], **combo_style, width=150)
    status_combobox.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    status_combobox.set("Available")

    movie_ctrl = MoviesCntrl()
    gates = movie_ctrl.get_available_gates()
    gate_values = [f"Gate {g['gate_id']} ({g['name']})" for g in gates] or ["No gates available"]
    gate_label = ctk.CTkLabel(row2, text="Cinema Gate", **label_style)
    gate_label.grid(row=0, column=3, sticky="w", padx=5, pady=(0, 2))
    gate_combobox = ctk.CTkComboBox(row2, values=gate_values, **combo_style, width=150)
    gate_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
    gate_combobox.set(gate_values[0] if gate_values else "No gates available")

    ctk.CTkLabel(content, text="Description", **label_style).pack(fill="x", padx=10, pady=(10, 0))
    description_text = ctk.CTkTextbox(content, height=140, fg_color="#E8FFD7", text_color="#3E5F44",
                                      border_color="#5E936C", corner_radius=6, wrap="word", font=("Book Antiqua", 12))
    description_text.pack(fill="both", expand=True, padx=10, pady=5)

    buttons_frame = ctk.CTkFrame(card, fg_color="#93DA97")
    buttons_frame.grid(row=1, column=0, pady=10)
    buttons_frame.grid_columnconfigure((0, 1), weight=1)

    def on_register():
        title = title_entry.get().strip()
        release_date = release_date_entry.get().strip()
        genre = genre_combobox.get().strip()
        price = price_entry.get().strip()
        duration = duration_entry.get().strip()
        rating = rating_combobox.get().strip()
        description = description_text.get("1.0", "end-1c").strip()
        poster_path = poster_filename["value"]
        status = status_combobox.get().strip()
        gate = gate_combobox.get().split(" ")[1].strip("()") if gate_combobox.get() != "No gates available" else None

        errors = {}
        try:
            price_float = float(price) if price.strip() else 0
            if price_float <= 0:
                errors["price"] = "Price must be a positive number."
        except ValueError:
            errors["price"] = "Price must be a number."
        try:
            duration_int = int(duration) if duration.strip() else 0
            if duration_int <= 0:
                errors["duration"] = "Duration must be a positive number."
        except ValueError:
            errors["duration"] = "Duration must be a number."
        try:
            if release_date:
                datetime.strptime(release_date, "%Y-%m-%d")
            else:
                errors["release_date"] = "Release date is required."
        except ValueError:
            errors["release_date"] = "Release date must be in YYYY-MM-DD format."
        if not title:
            errors["title"] = "Title is required."
        if not genre:
            errors["genre"] = "Genre is required."
        if not rating:
            errors["rating"] = "Rating is required."
        if not status:
            errors["status"] = "Status is required."
        if not description:
            errors["description"] = "Description is required."
        if not poster_path:
            errors["poster"] = "Poster is required."
        if not gate or gate == "No gates available":
            errors["gate"] = "A valid cinema gate is required."

        if errors:
            messagebox.showerror("Error", "\n".join(errors.values()))
            return

        movie_ctrl = MoviesCntrl(
            title=title,
            genre=genre,
            price=price_float,
            duration=duration_int,
            rating=rating,
            description=description,
            poster_path=poster_path,
            status=status,
            gate=gate,
            release_date=release_date
        )
        success, errors = movie_ctrl.AddMovie()
        if success:
            messagebox.showinfo("Success", f"Movie '{title}' registered and assigned to Gate {gate} successfully!")
            modal.destroy()
            if hasattr(self, 'refresh_movies'):
                self.refresh_movies()
        else:
            messagebox.showerror("Error", "\n".join(errors))

    register_btn = ctk.CTkButton(buttons_frame, text="Register Movie", command=on_register, **button_style, width=180)
    register_btn.grid(row=0, column=0, padx=5, pady=5)
    cancel_btn = ctk.CTkButton(buttons_frame, text="Cancel", command=modal.destroy,
                               font=("Book Antiqua", 13, "bold"), fg_color="#E8FFD7", hover_color="#5E936C",
                               text_color="#3E5F44", corner_radius=6, height=38, width=180)
    cancel_btn.grid(row=0, column=1, padx=5, pady=5)