import customtkinter as ctk

def message_modal(self, message: str, duration: int = 2000, success: bool = True):
    modal = ctk.CTkToplevel(self)
    modal.title("Message")
    modal.configure(fg_color="#F4F4F4")
    modal.transient(self)
    modal.grab_set()

    # Center small modal
    w, h = 350, 150
    parent_x = self.winfo_rootx()
    parent_y = self.winfo_rooty()
    parent_w = self.winfo_width()
    parent_h = self.winfo_height()
    x = parent_x + (parent_w // 2) - (w // 2)
    y = parent_y + (parent_h // 2) - (h // 2) - 15
    modal.geometry(f"{w}x{h}+{x}+{y}")

    # Card container
    card = ctk.CTkFrame(modal, fg_color="#FFFFFF", corner_radius=12)
    card.pack(expand=True, fill="both", padx=20, pady=20)

    # Label with message
    color = "#28a745" if success else "#dc3545"  # green or red
    ctk.CTkLabel(
        card,
        text=message,
        font=("Book Antiqua", 16, "bold"),
        text_color=color
    ).pack(expand=True, pady=20)

    # Auto-close after duration (ms)
    modal.after(duration, modal.destroy)
