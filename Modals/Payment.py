import customtkinter as ctk

def payment_modal(parent, ticket, pay_callback=None):
    modal = ctk.CTkToplevel(parent)
    modal.title("Payment Info")
    modal.configure(fg_color="#E8FFD7")
    modal.transient(parent)
    modal.grab_set()

    # Extract data safely from ticket
    movie_title = ticket.get("movie_title", "Unknown Movie")
    cinema = ticket.get("gate", "Unknown Cinema")
    seat = ticket.get("seat", "Unknown Seat")
    total_price = float(ticket.get("price", 0))
    showtime = ticket.get("showtime", "")

    # Try to split showtime into date/time
    if " " in showtime:
        date, time_range = showtime.split(" ", 1)
    else:
        date, time_range = showtime, "N/A"

    # Modal size & center
    w, h = 420, 420
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height()
    x = parent_x + (parent_w // 2) - (w // 2) -50
    y = parent_y + (parent_h // 2) - (h // 2)
    modal.geometry(f"{w}x{h}+{x}+{y}")
    modal.attributes('-topmost', True)

    # ===== CARD =====
    card = ctk.CTkFrame(modal, fg_color="#93DA97", corner_radius=15)
    card.pack(expand=True, fill="both", padx=20, pady=20)

    # ===== TITLE =====
    ctk.CTkLabel(
        card,
        text="Payment Info",
        font=("Book Antiqua", 20, "bold"),
        text_color="#3E5F44"
    ).pack(pady=(20, 15))

    # ===== SCROLLABLE AREA =====
    scrollable = ctk.CTkScrollableFrame(card, fg_color="#93DA97", corner_radius=10)
    scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    # ===== CONTENT =====
    def make_label(title, value_list):
        """Helper to create label groups with indentation."""
        ctk.CTkLabel(
            scrollable,
            text=title,
            font=("Book Antiqua", 14, "bold"),
            text_color="#3E5F44",
            anchor="w"
        ).pack(anchor="w", pady=(10, 0), padx=(5, 0))

        for val in value_list:
            ctk.CTkLabel(
                scrollable,
                text=f"• {val}",
                font=("Book Antiqua", 13),
                text_color="#3E5F44",
                anchor="w"
            ).pack(anchor="w", padx=(20, 0))  # Indent data

    make_label("Movie", [movie_title])
    make_label("Time & Date", [f"{date}", f"{time_range}"])
    make_label("Seat & Cinema", [cinema, seat])

    # ===== TOTAL =====
    ctk.CTkLabel(
        scrollable,
        text=f"Total: ₱{total_price}",
        font=("Book Antiqua", 14, "bold"),
        text_color="#3E5F44"
    ).pack(anchor="w", pady=(10, 0), padx=(5, 0))

    # Divider line
    ctk.CTkFrame(scrollable, fg_color="#3E5F44", height=1).pack(fill="x", pady=(5, 10), padx=(5, 0))

    # ===== CASH INPUT =====
    ctk.CTkLabel(
        scrollable,
        text="Cash Received:",
        font=("Book Antiqua", 13, "bold"),
        text_color="#3E5F44"
    ).pack(anchor="w", padx=(5, 0))

    cash_var = ctk.StringVar()
    entry = ctk.CTkEntry(
        scrollable,
        textvariable=cash_var,
        placeholder_text="Enter amount...",
        font=("Book Antiqua", 13),
        fg_color="#E8FFD7",
        text_color="#3E5F44",
        border_color="#5E936C",
        corner_radius=10,
        height=40
    )
    entry.pack(fill="x", pady=(5, 10), padx=(5, 5))

    # ===== CHANGE DISPLAY =====
    change_label = ctk.CTkLabel(
        scrollable,
        text="Change: ₱0.00",
        font=("Book Antiqua", 14, "bold"),
        text_color="#3E5F44"
    )
    change_label.pack(anchor="w", padx=(5, 0), pady=(5, 10))

    def update_change(*args):
        """Live change calculator."""
        try:
            cash = float(cash_var.get())
            change = cash - total_price
            if change < 0:
                change_label.configure(text="Change: ₱0.00", text_color="#B91C1C")
            else:
                change_label.configure(text=f"Change: ₱{change:.2f}", text_color="#3E5F44")
        except ValueError:
            change_label.configure(text="Change: ₱0.00", text_color="#B91C1C")

    cash_var.trace_add("write", update_change)

    # ===== CUSTOM SUCCESS MESSAGE CARD =====
    def show_success_message(change):
        msg_modal = ctk.CTkToplevel(modal)
        msg_modal.title("Payment Successful")
        msg_modal.configure(fg_color="#E8FFD7")
        msg_modal.geometry("300x180")
        msg_modal.transient(modal)
        msg_modal.grab_set()
        msg_modal.attributes('-topmost', True)

        frame = ctk.CTkFrame(msg_modal, fg_color="#93DA97", corner_radius=15)
        frame.pack(expand=True, fill="both", padx=15, pady=15)

        ctk.CTkLabel(
            frame,
            text="✅ Payment Successful!",
            font=("Book Antiqua", 16, "bold"),
            text_color="#3E5F44"
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            frame,
            text=f"Change: ₱{change:.2f}",
            font=("Book Antiqua", 14),
            text_color="#3E5F44"
        ).pack(pady=(5, 10))

        ctk.CTkButton(
            frame,
            text="OK",
            fg_color="#ef4444",
            hover_color="#dc2626",
            text_color="#E8FFD7",
            corner_radius=10,
            command=lambda: (msg_modal.destroy(), modal.destroy())
        ).pack(pady=(10, 15), ipadx=40)

    # ===== PAY BUTTON =====
    def pay_action():
        try:
            cash = float(entry.get())
            change = cash - total_price
            if cash < total_price:
                change_label.configure(text="Insufficient Amount", text_color="#B91C1C")
            else:
                # 🟢 Debug what’s being sent to controller
                if pay_callback:
                    payment_data = {
                        "ticket_id": ticket.get("ticket_id"),
                        "money": cash,
                        "change": change,
                        "method": "Cash",
                    }
                    print(f"[DEBUG] Sending to controller from modal: {payment_data}")
                    pay_callback(payment_data)

                show_success_message(change)
        except ValueError:
            change_label.configure(text="Invalid Amount", text_color="#B91C1C")

    pay_btn = ctk.CTkButton(
        card,
        text="Pay Cash",
        font=("Book Antiqua", 15, "bold"),
        fg_color="#ef4444",
        hover_color="#dc2626",
        text_color="#E8FFD7",
        corner_radius=10,
        height=45,
        command=pay_action
    )
    pay_btn.pack(pady=(5, 15), ipadx=80)

    modal.update()
    modal.lift()

    return entry, pay_btn
