from tkinter import *
import tkinter.messagebox
import time
import sqlite3


class ATM:
    def __init__(self, root):
        self.root = root
        blank_space = " "
        self.root.title(110 * blank_space + "ATM System")
        self.root.geometry("840x690+280+0")
        self.root.configure(background='gainsboro')

        # ======================================= Frames Setup =======================================
        # Creating the main container and sub-frames for the ATM interface layout

        mainfram = Frame(self.root, bd=20, width=790, height=700, relief=RIDGE)
        mainfram.grid()

        # Bottom frame for the numeric keypad
        topframe1 = Frame(mainfram, bd=7, width=734, height=300, relief=RIDGE)
        topframe1.grid(row=1, column=0, padx=12)

        # Top frame for the screen and side buttons
        topframe2 = Frame(mainfram, bd=7, width=734, height=300, relief=RIDGE)
        topframe2.grid(row=0, column=0, padx=8)

        # Left side buttons frame
        topframe2Left = Frame(topframe2, bd=5, width=340, height=300, relief=RIDGE)
        topframe2Left.grid(row=0, column=0, padx=3)

        # Middle frame for the ATM screen (Text widget)
        topframe2Mid = Frame(topframe2, bd=0, width=340, height=300, relief=RIDGE)
        topframe2Mid.grid(row=0, column=1, padx=3)

        # Right side buttons frame
        topframe2Right = Frame(topframe2, bd=5, width=340, height=300, relief=RIDGE)
        topframe2Right.grid(row=0, column=2, padx=3)

        # ====================================== Core Functions ====================================

        def login(pinN):
            """Connects to the SQLite database, verifies the PIN, and retrieves user data."""
            conn = sqlite3.connect('atm_system.db')
            cursor = conn.cursor()

            # Fetch user details and concatenate first and last name into a single string
            query = "SELECT pin_code, first_name || ' ' || last_name, balance, phone, city FROM users WHERE pin_code = ?"
            cursor.execute(query, (pinN,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return list(row)  # Return user data as a list if PIN is correct
            return 0  # Return 0 if user is not found

        def enter_Pin():
            """Handles PIN submission, checks validity, and navigates to the main menu if successful."""
            # Prevent ENTER button from executing if the user is already logged in
            if ATM.flag == 1:
                return

            pinNo = self.txtReceipt.get("5.2", "end-1c").strip()
            ATM.arr = login(pinNo)

            if ATM.arr != 0:
                self.txtReceipt.delete("1.0", END)
                ATM.flag = 1
                ATM.keypad_active = False  # Lock keypad on the main menu to prevent accidental typing

                # Display Main Menu
                self.txtReceipt.insert(END, "\t\t ATM" + "\n\n")
                self.txtReceipt.insert(END, "Withdraw Cash\t\t\t Loan" + "\n\n\n\n")
                self.txtReceipt.insert(END, "Cash With Receipt\t\t\t Deposit" + "\n\n\n\n")
                self.txtReceipt.insert(END, "Balance\t\t\t Request New Pin" + "\n\n\n\n")
                self.txtReceipt.insert(END, "Mini Statement\t\t\t print Statement" + "\n\n\n\n")
                self.txtReceipt.tag_config('word', font=600)
                WidgetNormal()  # Enable side buttons
            else:
                self.txtReceipt.delete("1.0", END)
                self.txtReceipt.insert(END, "\n\n\n\n\t Your PIN number is incorrect \n\n\n\t      Press \"CLEAR\" Button")

        def WidgetDisabale():
            """Disables all side arrow buttons (used during input screens)."""
            self.btnArrowR1 = Button(topframe2Right, width=160, height=60, state=DISABLED, command=loan,
                                     image=self.img_arrow_Right).grid(row=0, column=0, padx=2, pady=2)
            self.btnArrowR2 = Button(topframe2Right, width=160, height=60, state=DISABLED, command=deposit,
                                     image=self.img_arrow_Right).grid(row=1, column=0, padx=2, pady=2)
            self.btnArrowR3 = Button(topframe2Right, width=160, height=60, state=DISABLED, command=request_new_pin,
                                     image=self.img_arrow_Right).grid(row=2, column=0, padx=2, pady=2)
            self.btnArrowR4 = Button(topframe2Right, width=160, height=60, state=DISABLED, command=statement,
                                     image=self.img_arrow_Right).grid(row=3, column=0, padx=2, pady=2)

            self.btnArrowL1 = Button(topframe2Left, width=160, height=60, state=DISABLED, command=withdrawcach,
                                     image=self.img_arrow_Left).grid(row=0, column=0, padx=2, pady=4)
            self.btnArrowL2 = Button(topframe2Left, width=160, height=60, state=DISABLED, command=withdrawcach,
                                     image=self.img_arrow_Left).grid(row=1, column=0, padx=2, pady=4)
            self.btnArrowL3 = Button(topframe2Left, width=160, height=60, state=DISABLED, command=Balance,
                                     image=self.img_arrow_Left).grid(row=2, column=0, padx=2, pady=4)
            self.btnArrowL4 = Button(topframe2Left, width=160, height=60, state=DISABLED, command=Ministatement,
                                     image=self.img_arrow_Left).grid(row=3, column=0, padx=2, pady=4)

        def WidgetNormal():
            """Enables all side arrow buttons (used on the main menu)."""
            self.btnArrowR1 = Button(topframe2Right, width=160, height=60, state=NORMAL, command=loan,
                                     image=self.img_arrow_Right).grid(row=0, column=0, padx=2, pady=2)
            self.btnArrowR2 = Button(topframe2Right, width=160, height=60, state=NORMAL, command=deposit,
                                     image=self.img_arrow_Right).grid(row=1, column=0, padx=2, pady=2)
            self.btnArrowR3 = Button(topframe2Right, width=160, height=60, state=NORMAL, command=request_new_pin,
                                     image=self.img_arrow_Right).grid(row=2, column=0, padx=2, pady=2)
            self.btnArrowR4 = Button(topframe2Right, width=160, height=60, state=NORMAL, command=statement,
                                     image=self.img_arrow_Right).grid(row=3, column=0, padx=2, pady=2)

            self.btnArrowL1 = Button(topframe2Left, width=160, height=60, state=NORMAL, command=withdrawcach,
                                     image=self.img_arrow_Left).grid(row=0, column=0, padx=2, pady=4)
            self.btnArrowL2 = Button(topframe2Left, width=160, height=60, state=NORMAL, command=withdrawcach,
                                     image=self.img_arrow_Left).grid(row=1, column=0, padx=2, pady=4)
            self.btnArrowL3 = Button(topframe2Left, width=160, height=60, state=NORMAL, command=Balance,
                                     image=self.img_arrow_Left).grid(row=2, column=0, padx=2, pady=4)
            self.btnArrowL4 = Button(topframe2Left, width=160, height=60, state=NORMAL, command=Ministatement,
                                     image=self.img_arrow_Left).grid(row=3, column=0, padx=2, pady=4)

        def backNORMAL():
            """Restores the 'Back' button functionality on the keypad."""
            self.btnSp3 = Button(topframe1, width=160, height=60, stat=NORMAL, command=homePaje,
                                 image=self.imgSp3).grid(row=5, column=3, padx=6, pady=4)

        def clear():
            """Clears the screen, logs out the user, and cleans up dynamic widgets."""
            # Destroy any floating widgets (like dynamically placed 'next' buttons)
            for widget in self.root.place_slaves():
                widget.destroy()

            self.txtReceipt.delete("1.0", END)
            ATM.flag = 0
            ATM.keypad_active = True  # Unlock keypad for the login screen
            WidgetDisabale()
            self.txtReceipt.insert(END, "\n\t       Welcome to iBank\n\tplease enter you PIN number:\n\n\t\t")

        def insert(number):
            """Inserts a numeric character into the screen only if the keypad is active."""
            if ATM.keypad_active:
                self.txtReceipt.insert(END, number)

        def cancel():
            """Prompts the user to confirm exit and closes the application."""
            Cancel = tkinter.messagebox.askyesno("ATM", "Confirm if you want to cancel")
            if Cancel > 0:
                self.root.destroy()
                return

        def apdute(sumM, typeaction):
            """Records the transaction in the database and updates the user's balance."""
            pin = ATM.arr[0]
            new_balance = float(ATM.arr[2])
            current_date = time.strftime("%d/%m/%Y")
            current_time = time.strftime("%H:%M:%S")

            conn = sqlite3.connect('atm_system.db')
            cursor = conn.cursor()

            # Insert the action into the transactions history table
            cursor.execute('''
                INSERT INTO transactions (user_pin, action_date, action_time, action_type, amount)
                VALUES (?, ?, ?, ?, ?)
            ''', (pin, current_date, current_time, typeaction, float(sumM)))

            # Update the user's current balance in the users table
            cursor.execute('UPDATE users SET balance = ? WHERE pin_code = ?', (new_balance, pin))

            conn.commit()
            conn.close()

        def withdrawC(sumM, del1, del2, del3, del4, del5, del6, del7):
            """Validates the withdrawal amount, updates balance, and destroys dynamically created buttons."""
            blance = float(ATM.arr[2])
            if sumM > blance:
                tkinter.messagebox.showwarning("ATM", "Insufficient balance!")
                return 0

            blance -= sumM
            ATM.arr[2] = str(blance)  # Update local array
            apdute(sumM, "withdraw cach")  # Update database

            # Clean up UI buttons
            del1.destroy()
            del2.destroy()
            del3.destroy()
            del4.destroy()
            del5.destroy()
            del6.destroy()
            del7.destroy()
            homePaje()

        def Remove7(btn1, btn2, btn3, btn4, btn5, btn6, btn7):
            """Helper function to remove dynamic buttons and return to home page."""
            btn1.destroy()
            btn2.destroy()
            btn3.destroy()
            btn4.destroy()
            btn5.destroy()
            btn6.destroy()
            btn7.destroy()
            backNORMAL()
            homePaje()

        def withdrawcach():
            """Displays the cash withdrawal interface with pre-defined amount buttons."""
            ATM.keypad_active = False  # Lock keypad (user must use on-screen choices)
            self.txtReceipt.delete("1.0", END)
            WidgetDisabale()
            self.txtReceipt.insert(END, "\n\t      Welcome to iBank\n\n")
            self.txtReceipt.insert(END, "     enter the amount you want to withdraw:")

            # Dynamically placing withdrawal options
            btn1 = Button(root, text="20" + u"\u20AA", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: withdrawC(20, btn1, btn2, btn3, btn4, btn5, btn6, btn7))
            btn1.place(x=285, y=130)
            btn2 = Button(root, text="40" + u"\u20AA", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: withdrawC(40, btn1, btn2, btn3, btn4, btn5, btn6, btn7))
            btn2.place(x=405, y=130)
            btn3 = Button(root, text="60" + u"\u20AA", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: withdrawC(60, btn1, btn2, btn3, btn4, btn5, btn6, btn7))
            btn3.place(x=285, y=170)
            btn4 = Button(root, text="80" + u"\u20AA", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: withdrawC(80, btn1, btn2, btn3, btn4, btn5, btn6, btn7))
            btn4.place(x=405, y=170)
            btn5 = Button(root, text="100" + u"\u20AA", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: withdrawC(100, btn1, btn2, btn3, btn4, btn5, btn6, btn7))
            btn5.place(x=285, y=210)
            btn6 = Button(root, text="200" + u"\u20AA", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: withdrawC(200, btn1, btn2, btn3, btn4, btn5, btn6, btn7))
            btn6.place(x=405, y=210)
            btn7 = Button(root, text="300" + u"\u20AA", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: withdrawC(300, btn1, btn2, btn3, btn4, btn5, btn6, btn7))
            btn7.place(x=345, y=250)
            self.btnSp3 = Button(topframe1, width=160, height=60, stat=NORMAL,
                                 command=lambda: Remove7(btn1, btn2, btn3, btn4, btn5, btn6, btn7),
                                 image=self.imgSp3).grid(row=5, column=3, padx=6, pady=4)

        def Remove3(bt1, bt2, bt3):
            """Helper function to remove dynamic loan buttons."""
            bt1.destroy()
            bt2.destroy()
            bt3.destroy()
            backNORMAL()
            homePaje()

        def payloan(bt):
            """Validates the input loan amount and prompts the user to select an interest rate type."""
            try:
                amount_str = self.txtReceipt.get("5.2", "end-1c").strip()
                cash = float(amount_str)
            except ValueError:
                tkinter.messagebox.showwarning("ATM", "Please enter a valid amount")
                return

            ATM.keypad_active = False  # Lock keypad once the user is selecting the loan type
            self.txtReceipt.delete("1.0", END)
            bt.destroy()
            self.txtReceipt.insert(END, "\n        please select type of the availment :")

            # Dynamic buttons for loan terms (revolving, 36 months, 24 months)
            btn1 = Button(root, text="revolving\n2.50% / month", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: payloanEnd(cash, btn1, btn2, btn3, 1))
            btn1.place(x=285, y=90)
            btn2 = Button(root, text="term 36 months\n1.75% / month", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: payloanEnd(cash, btn1, btn2, btn3, 2))
            btn2.place(x=405, y=90)
            btn3 = Button(root, text="term 24 months\n1.75% / month", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: payloanEnd(cash, btn1, btn2, btn3, 3))
            btn3.place(x=405, y=140)

            self.btnSp3 = Button(topframe1, width=160, height=60, stat=NORMAL,
                                 command=lambda: Remove3(btn1, btn2, btn3), image=self.imgSp3).grid(row=5, column=3,
                                                                                                    padx=6, pady=4)

        def payloanEnd(cash, bt1, bt2, bt3, typeOfLoan):
            """Finalizes the loan application, updates the database, and cleans up the UI."""
            pin = ATM.arr[0]
            conn = sqlite3.connect('atm_system.db')
            cursor = conn.cursor()

            # Insert the loan details (including the selected type) into the specialized loans table
            cursor.execute('INSERT INTO loans (user_pin, loan_amount, loan_type) VALUES (?, ?, ?)',
                           (pin, float(cash), int(typeOfLoan)))
            conn.commit()
            conn.close()

            apdute(cash, "loan")  # Record as a standard transaction history event
            self.txtReceipt.delete("1.0", END)
            bt1.destroy()
            bt2.destroy()
            bt3.destroy()
            homePaje()

        def Remove1(bt):
            """Helper function to remove a single dynamic button."""
            bt.destroy()
            backNORMAL()
            homePaje()

        def loan():
            """Initializes the loan interface allowing the user to enter a desired amount."""
            ATM.keypad_active = True  # Unlock keypad to enter loan amount
            WidgetDisabale()
            self.txtReceipt.delete("1.0", END)
            self.txtReceipt.insert(END, "\n\n   please enter the amount you want to loan:\n\n\t\t")

            btn = Button(root, text="next", bg="light yellow", fg="red", width=10, padx=10,
                         command=lambda: payloan(btn))
            btn.place(x=340, y=150)
            self.btnSp3 = Button(topframe1, width=160, height=60, stat=NORMAL, command=lambda: Remove1(btn),
                                 image=self.imgSp3).grid(row=5, column=3, padx=6, pady=4)

        def depositCach(bt1):
            """Prepares the interface for the user to input the physical cash deposit amount."""
            ATM.keypad_active = True  # Unlock keypad to enter deposit amount
            self.txtReceipt.delete("1.0", END)
            bt1.destroy()
            self.txtReceipt.insert(END, "\n Please write the amount you want to deposit:\n\n\t\t")

            btn1 = Button(root, text="to deposit", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: end(btn1))
            btn1.place(x=340, y=135)
            self.btnSp3 = Button(topframe1, width=160, height=60, stat=NORMAL, command=lambda: Remove1(btn1),
                                 image=self.imgSp3).grid(row=5, column=3, padx=6, pady=4)

        def end(bt):
            """Validates the deposit amount, updates the balance, and logs the transaction."""
            try:
                amount_str = self.txtReceipt.get("4.2", "end-1c").strip()
                pinNo = float(amount_str)
                blan = float(ATM.arr[2])
                blan += pinNo
                ATM.arr[2] = str(blan)  # Update local array
                apdute(pinNo, "deposit")  # Update database
            except ValueError:
                tkinter.messagebox.showwarning("ATM", "Please enter a valid amount")
                return

            bt.destroy()
            homePaje()

        def deposit():
            """Displays deposit instructions to the user."""
            ATM.keypad_active = False  # Lock keypad on instruction screen
            WidgetDisabale()
            self.txtReceipt.delete("1.0", END)
            self.txtReceipt.insert(END, "\n\t      get your cash ready.\n")
            self.txtReceipt.insert(END, "\n          make sure it's flat and unfolded.\n")
            self.txtReceipt.insert(END, "\n    you can insert up to 50 bills at one times.\n")

            btn1 = Button(root, text="continue", bg="light yellow", fg="red", width=10, padx=10,
                          command=lambda: depositCach(btn1))
            btn1.place(x=340, y=160)
            self.btnSp3 = Button(topframe1, width=160, height=60, stat=NORMAL, command=lambda: Remove1(btn1),
                                 image=self.imgSp3).grid(row=5, column=3, padx=6, pady=4)

        def request_new_pin():
            """Displays a confirmation screen that a new PIN has been dispatched."""
            ATM.keypad_active = False
            WidgetDisabale()
            self.txtReceipt.delete("1.0", END)
            self.txtReceipt.insert(END, "\n         " + str(
                ATM.arr[1]) + " we send the new pin\n\tnumber to this phone number \n\t\t" + str(ATM.arr[3]))
            self.txtReceipt.insert(END, ".\n\n\n\n\n\n\n\n\n\n\n\n\n   thank for your patience iBank.")

        def Balance():
            """Displays the user's current account balance retrieved from the database."""
            ATM.keypad_active = False
            WidgetDisabale()
            self.txtReceipt.delete("1.0", END)
            self.txtReceipt.insert(END, "\n\n\t      Welcome to iBank\n\n")
            self.txtReceipt.insert(END,
                                   "       in Your bank account the balance is\n\n\t\t" + str(ATM.arr[2]) + u"\u20AA")

        def Ministatement():
            """Fetches and displays the 5 most recent transactions for the logged-in user."""
            ATM.keypad_active = False
            WidgetDisabale()
            self.txtReceipt.delete("1.0", END)
            self.txtReceipt.insert(END, "\n   name:  " + str(ATM.arr[1]) + ".")
            self.txtReceipt.insert(END, "\n   date:  " + time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime()) + "\n")
            self.txtReceipt.insert(END, "   here are your last 5 transactions.\n\n")

            # Connect to database and fetch the last 5 transactions (DESC order)
            conn = sqlite3.connect('atm_system.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT action_date, action_time, action_type, amount FROM transactions WHERE user_pin=? ORDER BY id DESC LIMIT 5',
                (ATM.arr[0],))
            rows = cursor.fetchall()
            conn.close()

            # Format and insert each row into the screen
            for row in rows:
                line = f"{row[0]}   {row[1]}   {row[2]}   {row[3]}\n"
                self.txtReceipt.insert(END, "   " + line)

        def statement():
            """Fetches and displays the entire transaction history for the logged-in user."""
            ATM.keypad_active = False
            WidgetDisabale()
            self.txtReceipt.delete("1.0", END)
            self.txtReceipt.insert(END, "\n   name:  " + str(ATM.arr[1]) + ".")
            self.txtReceipt.insert(END, "\n   date:  " + time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime()) + "\n")
            self.txtReceipt.insert(END, "   here are your all transactions.\n\n")

            # Connect to database and fetch all historical transactions
            conn = sqlite3.connect('atm_system.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT action_date, action_time, action_type, amount FROM transactions WHERE user_pin=? ORDER BY id DESC',
                (ATM.arr[0],))
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                line = f"{row[0]}   {row[1]}   {row[2]}   {row[3]}\n"
                self.txtReceipt.insert(END, "   " + line)

        def homePaje():
            """Resets the screen and navigates back to the main ATM menu."""
            if ATM.flag == 1:
                ATM.keypad_active = False  # Keep keypad locked on the main menu
                WidgetNormal()
                self.txtReceipt.delete("1.0", END)
                self.txtReceipt.insert(END, "\t\t ATM" + "\n\n")
                self.txtReceipt.insert(END, "Withdraw Cash\t\t\t Loan" + "\n\n\n\n")
                self.txtReceipt.insert(END, "Cash With Receipt\t\t\t Deposit" + "\n\n\n\n")
                self.txtReceipt.insert(END, "Balance\t\t\t Request New Pin" + "\n\n\n\n")
                self.txtReceipt.insert(END, "Mini Statement\t\t\t print Statement" + "\n\n\n\n")

        # ====================================== End Functions ==================================
        # ======================================= UI Initialization ==============================

        # Main ATM Screen setup
        self.txtReceipt = Text(topframe2, height=17, width=42, bd=12, font=('arial', 10, 'bold'), bg="light yellow")
        self.txtReceipt.grid(row=0, column=1)
        self.txtReceipt.insert(END, "\n\t       Welcome to iBank\n\tplease enter you PIN number:\n\n\t\t")

        # Load side button arrows
        self.img_arrow_Left = PhotoImage(file="ATM_Icon/lArrow.png")
        self.img_arrow_Right = PhotoImage(file="ATM_Icon/rArrow.png")
        WidgetDisabale()

        # =================================== Pin Number Keypad Setup ===================================================

        self.img1 = PhotoImage(file="ATM_Numbers/one.png")
        self.btn1 = Button(topframe1, width=160, height=60, command=lambda: insert(1), image=self.img1).grid(row=2,
                                                                                                             column=0,
                                                                                                             padx=6,
                                                                                                             pady=4)

        self.img2 = PhotoImage(file="ATM_Numbers/two.png")
        self.btn2 = Button(topframe1, width=160, height=60, command=lambda: insert(2), image=self.img2).grid(row=2,
                                                                                                             column=1,
                                                                                                             padx=6,
                                                                                                             pady=4)

        self.img3 = PhotoImage(file="ATM_Numbers/three.png")
        self.btn3 = Button(topframe1, width=160, height=60, command=lambda: insert(3), image=self.img3).grid(row=2,
                                                                                                             column=2,
                                                                                                             padx=6,
                                                                                                             pady=4)

        self.imgCE = PhotoImage(file="ATM_Icon/cancel.png")
        self.btnCancel = Button(topframe1, width=160, height=60, command=cancel, image=self.imgCE).grid(row=2, column=3,
                                                                                                        padx=6, pady=4)

        self.img4 = PhotoImage(file="ATM_Numbers/four.png")
        self.btn4 = Button(topframe1, width=160, height=60, command=lambda: insert(4), image=self.img4).grid(row=3,
                                                                                                             column=0,
                                                                                                             padx=4,
                                                                                                             pady=4)

        self.img5 = PhotoImage(file="ATM_Numbers/five.png")
        self.btn5 = Button(topframe1, width=160, height=60, command=lambda: insert(5), image=self.img5).grid(row=3,
                                                                                                             column=1,
                                                                                                             padx=6,
                                                                                                             pady=4)

        self.img6 = PhotoImage(file="ATM_Numbers/six.png")
        self.btn6 = Button(topframe1, width=160, height=60, command=lambda: insert(6), image=self.img6).grid(row=3,
                                                                                                             column=2,
                                                                                                             padx=6,
                                                                                                             pady=4)

        self.imgCL = PhotoImage(file="ATM_Icon/clear.png")
        self.btnCLear = Button(topframe1, width=160, height=60, command=clear, image=self.imgCL).grid(row=3, column=3,
                                                                                                      padx=6, pady=4)

        self.img7 = PhotoImage(file="ATM_Numbers/seven.png")
        self.btn7 = Button(topframe1, width=160, height=60, command=lambda: insert(7), image=self.img7).grid(row=4,
                                                                                                             column=0,
                                                                                                             padx=4,
                                                                                                             pady=4)

        self.img8 = PhotoImage(file="ATM_Numbers/eight.png")
        self.btn8 = Button(topframe1, width=160, height=60, command=lambda: insert(8), image=self.img8).grid(row=4,
                                                                                                             column=1,
                                                                                                             padx=6,
                                                                                                             pady=4)

        self.img9 = PhotoImage(file="ATM_Numbers/nine.png")
        self.btn9 = Button(topframe1, width=160, height=60, command=lambda: insert(9), image=self.img9).grid(row=4,
                                                                                                             column=2,
                                                                                                             padx=6,
                                                                                                             pady=4)

        self.imgEnter = PhotoImage(file="ATM_Icon/enter.png")
        self.btnEnter = Button(topframe1, width=160, height=60, command=enter_Pin, image=self.imgEnter).grid(row=4,
                                                                                                             column=3,
                                                                                                             padx=6,
                                                                                                             pady=4)

        self.imgSp1 = PhotoImage(file="ATM_Icon/empty.png")
        self.btnSp1 = Button(topframe1, width=160, height=60, image=self.imgSp1).grid(row=5, column=0, padx=4, pady=4)

        self.img0 = PhotoImage(file="ATM_Numbers/zero.png")
        self.btn0 = Button(topframe1, width=160, height=60, command=lambda: insert(0), image=self.img0).grid(row=5,
                                                                                                             column=1,
                                                                                                             padx=6,
                                                                                                             pady=4)

        self.imgSp2 = PhotoImage(file="ATM_Icon/empty.png")
        self.btnSp2 = Button(topframe1, width=160, height=60, image=self.imgSp2).grid(row=5, column=2, padx=6, pady=4)

        self.imgSp3 = PhotoImage(file="ATM_Icon/back.png")
        backNORMAL()


# ======================================= Application Execution ==============================
ATM.flag = 0
ATM.keypad_active = True  # Initialize the keypad as active (open) for the login screen.
ATM.arr = []

if __name__ == '__main__':
    root = Tk()
    application = ATM(root)
    root.mainloop()