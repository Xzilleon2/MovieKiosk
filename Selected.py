import tkinter as tk
import os
from PIL import Image, ImageTk

class SelectedScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#F4F4F4")

        self.controller = controller
        self.columnconfigure(0, weight=1) # responsive column
        self.columnconfigure(1, weight=0)  # responsive column
        self.rowconfigure(0, weight=0) # responsive row 1
        self.rowconfigure(1, weight=2) # responsive row 2

        #upper Frame ==============================================================
        upperFrame = tk.Frame(
            self,
            bg="#F4F4F4",
        )
        upperFrame.grid(row=0, column=0, sticky="nsew",)
        upperFrame.columnconfigure(0, weight=1)
        upperFrame.rowconfigure(0, weight=1)

        buttonCon = tk.Frame(
            upperFrame,
            bg="#F4F4F4",
        )
        buttonCon.grid(row=0, column=0, sticky="sw", padx=15)

        backButton = tk.Button(
            buttonCon,
            text="← BACK TO MENU",
            font=("Book Antiqua", 20),
            fg="#665050",
            bg="#F4F4F4",
            relief="flat",
            anchor="center",
            command=lambda: controller.show_frame("HomePage")
        )
        backButton.grid(row=0, column=0, sticky="sw", pady=30)

        # Main Content ===============================================================
        mainFrame = tk.Frame(
            self,
            bg="#F4F4F4",
        )
        mainFrame.grid(row=1, column=0, sticky="nsew", padx=(20,0))
        mainFrame.columnconfigure(0, weight=1) # responsive column 1
        mainFrame.columnconfigure(1, weight=2)  # responsive column 2
        mainFrame.rowconfigure(0, weight=1) # responsive row

        # Selected Image ===============================================================
        imgpath = os.path.join(os.path.dirname(__file__), "Assets", "PetSematary.png")
        img = Image.open(imgpath)
        img = img.resize((400, 600), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(img)

        imgLabel = tk.Label(
            mainFrame,
            image=self.img,
            bg="#F4F4F4",
        )
        imgLabel.grid(row=0, column=0, sticky="nsew")

        #Info Frame ===============================================================
        infoFrame = tk.Frame(
            mainFrame,
            bg="#F4F4F4",
        )
        infoFrame.grid(row=0, column=1, sticky="nsew")
        infoFrame.rowconfigure(0, weight=0) # responsive title
        infoFrame.rowconfigure(1, weight=0) # responsive description
        infoFrame.rowconfigure(2, weight=0) # responsive Seat Frame
        infoFrame.rowconfigure(3, weight=0) # responsive time Frame
        infoFrame.rowconfigure(4, weight=0) # responsive Price Frame
        infoFrame.rowconfigure(5, weight=0) # responsive button Frame
        infoFrame.columnconfigure(0, weight=1) # responsive column

        titleLabel = tk.Label(
            infoFrame,
            text="Pet Sematary",
            font=("Book Antiqua", 40),
            fg="#665050",
            bg="#F4F4F4",
            anchor="w"
        )
        titleLabel.grid(row=0, column=0, sticky="new", pady=(70,0))

        descriptionLabel = tk.Label(
            infoFrame,
            text=(
                "Richard, an archaeologist and professor, and his wife, Jules, "
                "live with their young son Owen on Richard's deceased father's isolated farm on the moors. "
                "Owen, an asthmatic child, tells his mother...."
            ),
            font=("Book Antiqua", 12),
            fg="#665050",
            bg="#F4F4F4",
            anchor="nw",
            justify="left",  # text alignment
            wraplength=700  # max width in pixels before wrapping
        )
        descriptionLabel.grid(row=1, column=0, sticky="new")

        # Seat Frame ============================================================
        seatFrame = tk.Frame(
            infoFrame,
            bg="#F4F4F4",
        )
        seatFrame.grid(row=2, column=0, sticky="nsew", pady=(20,0))
        seatFrame.rowconfigure(0, weight=1)
        seatFrame.rowconfigure(1, weight=2)
        seatFrame.columnconfigure(0, weight=1)

        seatLabel = tk.Label(
            seatFrame,
            text="AVAILABLE SEATS",
            font=("Book Antiqua", 12),
            bg="#F4F4F4",
            fg="#998F8F",
            anchor="w",
        )
        seatLabel.grid(row=0, column=0, sticky="nsew", padx=(0,30))

        seatFrameCon = tk.Frame(
            seatFrame,
            bg="#F4F4F4",
        )
        seatFrameCon.grid(row=1, column=0, sticky="nsew")

        seatButton1 = tk.Button(
            seatFrameCon,
            text="A1",
            font=("Book Antiqua", 14),
            fg="#665050",
            bg="#EFE9E0",
            relief=tk.GROOVE,
        )
        seatButton1.pack(side=tk.LEFT, anchor=tk.N, padx=(0,10))

        seatButton2 = tk.Button(
            seatFrameCon,
            text="A2",
            font=("Book Antiqua", 14),
            fg="#665050",
            bg="#EFE9E0",
            relief=tk.GROOVE,
        )
        seatButton2.pack(side=tk.LEFT, anchor=tk.N, padx=(0,10))

        # Time Frame ============================================================
        timeFrame = tk.Frame(
            infoFrame,
            bg="#F4F4F4",
        )
        timeFrame.grid(row=3, column=0, sticky="nsew",)
        timeFrame.rowconfigure(0, weight=1)
        timeFrame.rowconfigure(1, weight=1)
        timeFrame.columnconfigure(0, weight=1)

        timeLabel = tk.Label(
            timeFrame,
            text="TIME",
            font=("Book Antiqua", 12),
            bg="#F4F4F4",
            fg="#998F8F",
            anchor="sw",
        )
        timeLabel.grid(row=0, column=0, sticky="nsew", padx=(0,30), pady=10)

        timeFrameCon = tk.Frame(
            timeFrame,
            bg="#F4F4F4",
        )
        timeFrameCon.grid(row=1, column=0, sticky="nsew")

        timeButton1 = tk.Button(
            timeFrameCon,
            text="1:00 - 2:00",
            font=("Book Antiqua", 14),
            fg="#665050",
            bg="#EFE9E0",
            relief=tk.GROOVE,
        )
        timeButton1.pack(side=tk.LEFT, anchor=tk.N, padx=(0,10))

        timeButton2 = tk.Button(
            timeFrameCon,
            text="2:00 - 3:00",
            font=("Book Antiqua", 14),
            fg="#665050",
            bg="#EFE9E0",
            relief=tk.GROOVE,
        )
        timeButton2.pack(side=tk.LEFT, anchor=tk.N, padx=(0,10))

        # Gate Frame ============================================================
        gateFrame = tk.Frame(
            infoFrame,
            bg="#F4F4F4",
        )
        gateFrame.grid(row=4, column=0, sticky="nsew",)
        gateFrame.rowconfigure(0, weight=1)
        gateFrame.rowconfigure(1, weight=1)
        gateFrame.columnconfigure(0, weight=1)

        gateLabel = tk.Label(
            gateFrame,
            text="GATE",
            font=("Book Antiqua", 12),
            bg="#F4F4F4",
            fg="#998F8F",
            anchor="sw",
        )
        gateLabel.grid(row=0, column=0, sticky="nsew", padx=(0,30), pady=10)

        gateFrameCon = tk.Frame(
            gateFrame,
            bg="#F4F4F4",
        )
        gateFrameCon.grid(row=1, column=0, sticky="nsew")

        gateButton1 = tk.Button(
            gateFrameCon,
            text="Gate 1",
            font=("Book Antiqua", 14),
            fg="#665050",
            bg="#EFE9E0",
            relief=tk.GROOVE,
        )
        gateButton1.pack(side=tk.LEFT, anchor=tk.N, padx=(0,10))

        gateButton2 = tk.Button(
            gateFrameCon,
            text="Gate 2",
            font=("Book Antiqua", 14),
            fg="#665050",
            bg="#EFE9E0",
            relief=tk.GROOVE,
        )
        gateButton2.pack(side=tk.LEFT, anchor=tk.N, padx=(0,10))

        # Price Frame ============================================================
        priceCon = tk.Frame(
            infoFrame,
            bg="#F4F4F4",
        )
        priceCon.grid(row=5, column=0, sticky="nsew", pady=20)
        priceCon.rowconfigure(0, weight=1)
        priceCon.columnconfigure(0, weight=1)

        priceLabel = tk.Label(
            priceCon,
            text="$300",
            font=("Book Antiqua", 30),
            fg="#665050",
        )
        priceLabel.pack(side=tk.LEFT, anchor=tk.N)

        # Purchase Frame ============================================================
        purchaseCon = tk.Frame(
            infoFrame,
            bg="#F4F4F4",
        )
        purchaseCon.grid(row=6, column=0, sticky="nsew", pady=10)
        purchaseCon.rowconfigure(0, weight=1)
        purchaseCon.columnconfigure(0, weight=1)

        purchaseBtn = tk.Button(
            purchaseCon,
            width= 20 ,
            text="Place Order",
            font=("Book Antiqua", 14),
            fg="#FFFFFF",
            bg="#CD4126",
            command=self.open_modal
        )
        purchaseBtn.pack(side=tk.LEFT, ipady=5)

        # Modal Frame for the order details =====================================================
        self.orderFrame = tk.Frame(
            self,
            bg="#FFFFFF",
            width=250,
            bd=1,
            relief=tk.RAISED,
        )
        self.orderFrame.grid(row=0, column=1, rowspan=2, sticky="ns")
        self.orderFrame.columnconfigure(0, weight=1)
        self.orderFrame.rowconfigure(0, weight=0)
        self.orderFrame.rowconfigure(1, weight=1)
        self.orderFrame.rowconfigure(2, weight=1)
        self.orderFrame.rowconfigure(3, weight=0)
        self.orderFrame.rowconfigure(4, weight=0)

        # keep width fixed, allow height to expand
        self.orderFrame.grid_propagate(False)
        self.orderFrame.grid_remove()  # hide initially

    def open_modal(self):
        # Show the orderFrame
        self.orderFrame.grid()

        # Clear old contents
        for widget in self.orderFrame.winfo_children():
            widget.destroy()

        # Fill with order info
        tk.Label(
            self.orderFrame,
            text="Order Status",
            font=("Book Antiqua", 24),
            bg="#FFFFFF",
            fg="#665050",
            anchor="nw",
        ).grid(row=0, column=0, sticky="nsew", padx=10, pady=(25,0))

        tk.Label(
            self.orderFrame,
            text="Tickets added",
            font=("Book Antiqua", 18),
            bg="#FFFFFF",
            fg="#665050",
            anchor="nw",
        ).grid(row=1, column=0, sticky="nsew", padx=(20,10), pady=(20,0))

        # Loop the content Here for tickets
        ticketFrame = tk.Frame(
            self.orderFrame,
            bg="#FFFFFF",
        )
        ticketFrame.grid(row=2, column=0, sticky="nsew", padx=(30,10), pady=(15,0))
        ticketFrame.columnconfigure(0, weight=1)
        ticketFrame.rowconfigure(0, weight=1)

        # Frame for Checkout Btn
        checkoutFrame = tk.Frame(
            self.orderFrame,
            bg="#FFFFFF",
        )
        checkoutFrame.grid(row=4, column=0, sticky="nsew", padx=(30,10), pady=(0,55))
        checkoutFrame.columnconfigure(0, weight=1)
        checkoutFrame.rowconfigure(0, weight=1)

        checkoutLabel = tk.Label(
            self.orderFrame,
            text="Total:",
            font=("Book Antiqua", 18),
            fg="#665050",
            bg="#FFFFFF",
            anchor="w",
        )
        checkoutLabel.grid(row=3, column=0, sticky="nsew", padx=(30,10), pady=(0,15))

        checkoutBtn = tk.Button(
            checkoutFrame,
            width= 10,
            text="Checkout",
            font=("Book Antiqua", 12),
            fg="#FFFFFF",
            bg="#CD4126",
            command=lambda: self.controller.show_frame("OrderCodeScreen")
        )
        checkoutBtn.pack(side=tk.LEFT)

