import os
from datetime import datetime

class ReceiptGenerator:
    def __init__(self, save_dir="Receipts"):
        # Create directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.save_dir = save_dir

    def generate_receipt(self, payment_data, ticket_data):
        """
        Generates a formatted text receipt and saves it to the Receipts folder.
        """
        # File name example: Receipt_A001_20251006_101530.txt
        filename = f"Receipt_{ticket_data['code']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.save_dir, filename)

        # Format receipt content
        content = f"""
        ============================================
                       Payment Receipt
        ============================================

        Movie: {ticket_data['movie_title']}
        Date: {datetime.now().strftime('%B %d, %Y')}
        Time: {datetime.now().strftime('%I:%M %p')}

        Cinema: {ticket_data['gate']}
        Seat: {ticket_data['seat']}

        Transaction Code: {ticket_data['code']}

        --------------------------------------------
        Amount:         ₱{ticket_data['price']:.2f}
        Customer Cash:  ₱{payment_data['money']:.2f}
        Change:         ₱{payment_data['change']:.2f}
        --------------------------------------------

        Thank you for choosing our cinema!
        Enjoy your movie 🎬
        ============================================

        Stub:
        {ticket_data['movie_title']} | {ticket_data['gate']} | {ticket_data['seat']}
        --------------------------------------------
        """

        # Save to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())

        print(f"[DEBUG] Receipt saved: {filepath}")
        return filepath
