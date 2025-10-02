import customtkinter as ctk
from tkinter import messagebox
from Classes.MoviesCntrl_Class import MoviesCntrl

def delete_modal(parent, movie_id, movie_title):
    # Create the modal
    modal = ctk.CTkToplevel(parent)
    modal.title("Confirm Deletion")
    modal.configure(fg_color="#E8FFD7")
    modal.transient(parent)  # Make modal stay on top of parent
    modal.grab_set()  # Ensure modal has focus

    # Modal size & center on screen
    w, h = 300, 150  # Fixed size
    screen_width = modal.winfo_screenwidth()
    screen_height = modal.winfo_screenheight()
    x = (screen_width // 2) - (w // 2)
    y = (screen_height // 2) - (h // 2)
    modal.geometry(f"{w}x{h}+{x}+{y}")

    # Create a frame for content
    content_frame = ctk.CTkFrame(modal, fg_color="#93DA97")
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Add label
    ctk.CTkLabel(
        content_frame,
        text=f"Delete movie '{movie_title}'?",
        font=("Book Antiqua", 16),
        text_color="#3E5F44"
    ).pack(pady=20)

    # Create a frame for buttons
    buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    buttons_frame.pack(pady=10, fill="x")

    def on_delete():
        moviescntrl = MoviesCntrl(movie_id=movie_id)
        ok = moviescntrl.deleteMovie()

        if ok:
            messagebox.showinfo("Success", f"Movie '{movie_title}' deleted successfully!")
            modal.destroy()
            parent.refresh_movies()
        else:
            messagebox.showerror("Error", f"Failed to delete movie '{movie_title}'.")
            modal.after(2000, modal.destroy)  # Close after 2 seconds

    # Define button styles
    delete_button_style = {
        "text": "Confirm",
        "font": ("Book Antiqua", 12),
        "fg_color": "#ef4444",
        "hover_color": "#dc2626",
        "text_color": "#E8FFD7",
        "width": 100,
        "height": 30
    }
    cancel_button_style = {
        "text": "Cancel",
        "font": ("Book Antiqua", 12),
        "fg_color": "#3E5F44",
        "hover_color": "#5E936C",
        "text_color": "#E8FFD7",
        "width": 100,
        "height": 30,
        "command": modal.destroy
    }

    # Create buttons
    delete_btn = ctk.CTkButton(buttons_frame, command=on_delete, **delete_button_style)
    delete_btn.pack(side="left", padx=(25, 5))

    cancel_btn = ctk.CTkButton(buttons_frame, **cancel_button_style)
    cancel_btn.pack(side="right", padx=(5, 25))

    # Ensure modal is focused
    modal.update()
    modal.lift()