import customtkinter as ctk
from tkinter import messagebox
from Classes.TicketCntrl_Class import TicketCntrl

def cancel_modal(parent, ticket_id, code):
    print(f"[DEBUG] cancel_modal() opened for ticket_id={ticket_id}, code='{code}'")

    modal = ctk.CTkToplevel(parent)
    modal.title("Confirm Cancellation")
    modal.configure(fg_color="#E8FFD7")
    modal.transient(parent)
    modal.grab_set()

    w, h = 300, 150
    screen_width = modal.winfo_screenwidth()
    screen_height = modal.winfo_screenheight()
    x = (screen_width // 2) - (w // 2)
    y = (screen_height // 2) - (h // 2)
    modal.geometry(f"{w}x{h}+{x}+{y}")

    content_frame = ctk.CTkFrame(modal, fg_color="#93DA97")
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    ctk.CTkLabel(
        content_frame,
        text=f"Cancel Ticket '{code}'?",
        font=("Book Antiqua", 16),
        text_color="#3E5F44"
    ).pack(pady=20)

    buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    buttons_frame.pack(pady=10, fill="x")

    def on_delete():
        print(f"[DEBUG] Confirm clicked — attempting to cancel ticket_id={ticket_id}")
        ticketcntrl = TicketCntrl()

        ok = ticketcntrl.cancel_ticket(ticket_id)
        print(f"[DEBUG] cancel_ticket() returned: {ok}")

        if ok:
            messagebox.showinfo("Success", f"Ticket '{code}' cancelled successfully!", parent=modal)
            modal.destroy()
            if hasattr(parent, "refresh_movies"):
                parent.refresh_movies()
            elif hasattr(parent, "refresh_tickets"):
                parent.refresh_tickets()
        else:
            messagebox.showerror("Error", f"Failed to cancel ticket '{code}'.", parent=modal)
            modal.after(2000, modal.destroy)

    delete_btn = ctk.CTkButton(
        buttons_frame,
        text="Confirm",
        font=("Book Antiqua", 12),
        fg_color="#ef4444",
        hover_color="#dc2626",
        text_color="#E8FFD7",
        width=100,
        height=30,
        command=on_delete
    )
    delete_btn.pack(side="left", padx=(25, 5))

    cancel_btn = ctk.CTkButton(
        buttons_frame,
        text="Cancel",
        font=("Book Antiqua", 12),
        fg_color="#3E5F44",
        hover_color="#5E936C",
        text_color="#E8FFD7",
        width=100,
        height=30,
        command=modal.destroy
    )
    cancel_btn.pack(side="right", padx=(5, 25))

    modal.update()
    modal.lift()
