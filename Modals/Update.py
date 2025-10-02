import customtkinter as ctk
from Classes.MoviesCntrl_Class import MoviesCntrl
from Classes.Movies_Class import Movies
from tkinter import filedialog, messagebox
from PIL import Image
import os
import shutil
from datetime import datetime, timedelta

def update_modal(self, movie_id, title, genre, price, duration, rating, status, description, poster):
    modal = ctk.CTkToplevel(self)
    modal.title("Update Movie")
    modal.configure(fg_color="#E8FFD7")
    modal.transient(self)
    modal.grab_set()

    w, h = 520, 720
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

    content = ctk.CTkFrame(card, fg_color="#93DA97")
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

    assets_dir = os.path.join(os.getcwd(), "Assets", "Posters")
    os.makedirs(assets_dir, exist_ok=True)
    poster_filename = {"value": poster}

    if poster:
        try:
            img_path = os.path.join(assets_dir, poster)
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img.thumbnail((180, 200))
                ctk_img = ctk.CTkImage(light_image=img, size=(180, 200))
                poster_preview.configure(image=ctk_img, text="")
                poster_preview.image = ctk_img
            else:
                poster_preview.configure(text="Poster not found")
        except Exception as e:
            print(f"Error loading poster: {e}")
            poster_preview.configure(text="Error loading poster")

    def upload_poster():
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file:
            fname = os.path.basename(file)
            dest = os.path.join(assets_dir, fname)
            shutil.copy(file, dest)
            poster_filename["value"] = fname
            try:
                img = Image.open(file)
                img.thumbnail((180, 200))
                ctk_img = ctk.CTkImage(light_image=img, size=(180, 200))
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
    title_entry.insert(0, title)

    row1 = ctk.CTkFrame(content, fg_color="#93DA97")
    row1.pack(fill="x", padx=10, pady=5)
    row1.grid_columnconfigure((0, 1), weight=1)

    duration_label = ctk.CTkLabel(row1, text="Duration (mins)", **label_style)
    duration_label.grid(row=0, column=0, sticky="w", padx=5, pady=(0, 2))
    duration_entry = ctk.CTkEntry(row1, **entry_style, width=220)
    duration_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    duration_entry.insert(0, duration)

    price_label = ctk.CTkLabel(row1, text="Price", **label_style)
    price_label.grid(row=0, column=1, sticky="w", padx=5, pady=(0, 2))
    price_entry = ctk.CTkEntry(row1, **entry_style, width=220)
    price_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    price_entry.insert(0, price)

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
    genre_combobox.set(genre or "Action | Adventure")

    rating_label = ctk.CTkLabel(row2, text="Rating", **label_style)
    rating_label.grid(row=0, column=1, sticky="w", padx=5, pady=(0, 2))
    rating_combobox = ctk.CTkComboBox(row2, values=["G", "PG", "PG-13", "R", "NC-17"], **combo_style, width=150)
    rating_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    rating_combobox.set(rating or "PG")

    status_label = ctk.CTkLabel(row2, text="Status", **label_style)
    status_label.grid(row=0, column=2, sticky="w", padx=5, pady=(0, 2))
    status_combobox = ctk.CTkComboBox(row2, values=["Available", "NotAvailable"], **combo_style, width=150)
    status_combobox.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    status_combobox.set(status or "Available")

    gate_label = ctk.CTkLabel(row2, text="Cinema Gate", **label_style)
    gate_label.grid(row=0, column=3, sticky="w", padx=5, pady=(0, 2))
    gate_combobox = ctk.CTkComboBox(row2, values=["Gate 1", "Gate 2", "Gate 3", "Gate 4"], **combo_style, width=150)
    gate_combobox.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
    gate_combobox.set("Gate 1")

    ctk.CTkLabel(content, text="Description", **label_style).pack(fill="x", padx=10, pady=(10, 0))
    description_text = ctk.CTkTextbox(content, height=140, fg_color="#E8FFD7", text_color="#3E5F44",
                                      border_color="#5E936C", corner_radius=6, wrap="word", font=("Book Antiqua", 12))
    description_text.pack(fill="both", expand=True, padx=10, pady=5)
    description_text.insert("1.0", description)

    buttons_frame = ctk.CTkFrame(card, fg_color="#93DA97")
    buttons_frame.grid(row=1, column=0, pady=10)
    buttons_frame.grid_columnconfigure((0, 1), weight=1)

    def on_update():
        updated_title = title_entry.get().strip()
        updated_genre = genre_combobox.get().strip()
        updated_price = price_entry.get().strip()
        updated_duration = duration_entry.get().strip()
        updated_rating = rating_combobox.get().strip()
        updated_description = description_text.get("1.0", "end-1c").strip()
        updated_poster = poster_filename["value"]
        updated_status = status_combobox.get().strip()
        updated_gate = gate_combobox.get().strip().split()[1]

        errors = {}
        try:
            price_float = float(updated_price) if updated_price.strip() else 0
            if price_float <= 0:
                errors["price"] = "Price must be a positive number."
        except ValueError:
            errors["price"] = "Price must be a number."
        try:
            duration_int = int(updated_duration) if updated_duration.strip() else 0
            if duration_int <= 0:
                errors["duration"] = "Duration must be a positive number."
        except ValueError:
            errors["duration"] = "Duration must be a number."
        if not updated_title:
            errors["title"] = "Title is required."
        if not updated_genre:
            errors["genre"] = "Genre is required."
        if not updated_rating:
            errors["rating"] = "Rating is required."
        if not updated_status:
            errors["status"] = "Status is required."
        if not updated_description:
            errors["description"] = "Description is required."
        if not updated_poster:
            errors["poster"] = "Poster is required."
        if not movie_id or not isinstance(movie_id, int) or movie_id <= 0:
            errors["movie_id"] = "Invalid movie ID."

        if errors:
            messagebox.showerror("Error", "\n".join(errors.values()))
            return

        start_date = datetime(2025, 10, 3, 1, 32).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        end_date = start_date + timedelta(days=30)
        movie_model = Movies()
        if not movie_model._IsGateAvailableForMonth(int(updated_gate), start_date, end_date):
            messagebox.showerror("Error", f"Gate {updated_gate} is not available for the entire month.")
            return

        conn = movie_model._connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Showtimes WHERE movie_id = %s", (movie_id,))
            conn.commit()
            cursor.close()
            conn.close()

        movie_ctrl = MoviesCntrl(title=updated_title, genre=updated_genre, price=price_float, duration=duration_int,
                                 rating=updated_rating, description=updated_description, poster_path=updated_poster,
                                 status=updated_status, movie_id=movie_id, gate=updated_gate)
        if movie_ctrl.UpdateMovie():
            showtimes_per_day = [10, 14, 18]
            available_seats = movie_model._GetGateCapacity(int(updated_gate))
            start_date = start_date.replace(hour=10, minute=0)

            for day in range(30):
                for hour in showtimes_per_day:
                    start_time = start_date.replace(hour=hour) + timedelta(days=day)
                    end_time = start_time + timedelta(minutes=int(duration_int) + 15)
                    if not movie_model._InsertShowtime(movie_id, int(updated_gate), start_time, end_time, available_seats):
                        messagebox.showerror("Error", f"Failed to schedule showtime for '{updated_title}' on {start_time}.")
                        return

            messagebox.showinfo("Success", f"Movie '{updated_title}' updated and assigned to Gate {updated_gate} successfully!")
            modal.destroy()
            self.refresh_movies()
        else:
            messagebox.showerror("Error", f"Failed to update movie '{updated_title}'.")
            modal.after(2000, modal.destroy)

    update_btn = ctk.CTkButton(buttons_frame, text="Update Movie", command=on_update, **button_style, width=180)
    update_btn.grid(row=0, column=0, padx=5, pady=5)
    cancel_btn = ctk.CTkButton(buttons_frame, text="Cancel", command=modal.destroy,
                               font=("Book Antiqua", 13, "bold"), fg_color="#E8FFD7", hover_color="#5E936C",
                               text_color="#3E5F44", corner_radius=6, height=38, width=180)
    cancel_btn.grid(row=0, column=1, padx=5, pady=5)