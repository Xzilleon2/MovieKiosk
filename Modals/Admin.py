import customtkinter as ctk
from tkinter import messagebox
from Classes.UserCntrl_Class import UserCntrl

def admin_login_modal(parent, controller):
    modal = ctk.CTkToplevel(parent)
    modal.title("Admin Login")
    modal.configure(fg_color="#E8FFD7")
    modal.transient(parent)
    modal.grab_set()

    # Modal size & center it
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

    card = ctk.CTkFrame(modal, fg_color="#93DA97", corner_radius=15)
    card.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(
        card,
        text="Admin Access",
        font=("Book Antiqua", 20, "bold"),
        text_color="#3E5F44"
    ).pack(pady=(25, 15))

    ctk.CTkLabel(card, text="Email", font=("Book Antiqua", 12), text_color="#3E5F44", anchor="w").pack(anchor="w", padx=25, pady=(10, 0))
    email_entry = ctk.CTkEntry(card, font=("Book Antiqua", 12), fg_color="#E8FFD7", text_color="#3E5F44",
                                border_color="#5E936C", corner_radius=10, height=40,
                                placeholder_text="Enter email", placeholder_text_color="#3E5F44")
    email_entry.pack(fill="x", padx=25, pady=5)

    ctk.CTkLabel(card, text="Password", font=("Book Antiqua", 12), text_color="#3E5F44", anchor="w").pack(anchor="w", padx=25, pady=(10, 0))
    password_entry = ctk.CTkEntry(card, font=("Book Antiqua", 12), fg_color="#E8FFD7", text_color="#3E5F44",
                                   border_color="#5E936C", corner_radius=10, height=40, show="*",
                                   placeholder_text="Enter password", placeholder_text_color="#3E5F44")
    password_entry.pack(fill="x", padx=25, pady=5)

    user_ctrl = UserCntrl()

    def attempt_login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        print(f"Email: {email}, Password: {password}")

        user = user_ctrl.login(email, password)
        if user:
            if user['roles'] == 'Admin':
                modal.destroy()
                controller.show_frame("AdminPage")
            else:
                messagebox.showerror("Access Denied", "You do not have permission to access Admin.", parent=modal)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.", parent=modal)

    login_btn = ctk.CTkButton(card, text="Sign In", font=("Book Antiqua", 14, "bold"),
                               fg_color="#3E5F44", hover_color="#5E936C", text_color="#E8FFD7",
                               corner_radius=10, height=45, command=attempt_login)
    login_btn.pack(pady=25, ipadx=70)

    return email_entry, password_entry, login_btn
