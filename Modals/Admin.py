import customtkinter as ctk

def admin_login_modal(parent, controller):
    modal = ctk.CTkToplevel(parent)
    modal.title("Admin Login")
    modal.configure(fg_color="#E8FFD7")  # Light green background
    modal.transient(parent)
    modal.grab_set()

    # Modal size & center it with slight animation
    w, h = 420, 380
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height()
    x = parent_x + (parent_w // 2) - (w // 2)
    y = parent_y + (parent_h // 2) - (h // 2)
    modal.geometry(f"{w}x{h}+{x}+{y}")
    modal.update()
    modal.attributes('-topmost', True)

    # ====== CARD CONTAINER ======
    card = ctk.CTkFrame(modal, fg_color="#93DA97", corner_radius=15)  # Secondary green for card
    card.pack(expand=True, fill="both", padx=20, pady=20)

    # Title with modern placement
    ctk.CTkLabel(
        card,
        text="Admin Access",
        font=("Book Antiqua", 20, "bold"),
        text_color="#3E5F44"  # Dark green text
    ).pack(pady=(25, 15))

    # Username
    ctk.CTkLabel(
        card,
        text="Username",
        font=("Book Antiqua", 12),
        text_color="#3E5F44",  # Dark green text
        anchor="w"
    ).pack(anchor="w", padx=25, pady=(10, 0))
    username_entry = ctk.CTkEntry(
        card,
        font=("Book Antiqua", 12),
        fg_color="#E8FFD7",  # Light green background
        text_color="#3E5F44",  # Dark green text
        border_color="#5E936C",  # Hover green for border
        corner_radius=10,
        height=40,
        placeholder_text="Enter username",
        placeholder_text_color="#3E5F44"
    )
    username_entry.pack(fill="x", padx=25, pady=5)

    # Password
    ctk.CTkLabel(
        card,
        text="Password",
        font=("Book Antiqua", 12),
        text_color="#3E5F44",  # Dark green text
        anchor="w"
    ).pack(anchor="w", padx=25, pady=(10, 0))
    password_entry = ctk.CTkEntry(
        card,
        font=("Book Antiqua", 12),
        fg_color="#E8FFD7",  # Light green background
        text_color="#3E5F44",  # Dark green text
        border_color="#5E936C",  # Hover green for border
        corner_radius=10,
        height=40,
        show="*",
        placeholder_text="Enter password",
        placeholder_text_color="#3E5F44"
    )
    password_entry.pack(fill="x", padx=25, pady=5)

    # Login Button with hover animation
    login_btn = ctk.CTkButton(
        card,
        text="Sign In",
        font=("Book Antiqua", 14, "bold"),
        fg_color="#3E5F44",  # Dark green button
        hover_color="#5E936C",  # Hover green
        text_color="#E8FFD7",  # Light green text
        corner_radius=10,
        height=45,
        command=lambda: [controller.show_frame("AdminPage"), modal.destroy()]
    )
    login_btn.pack(pady=25, ipadx=70)

    return username_entry, password_entry, login_btn