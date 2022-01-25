from tkinter import*
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk
import mysql.connector


def startpgm():
    "This function starts the program"
    win = Tk()
    app = SignInPage(win)
    win.mainloop()


class SignInPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1520x880+0+0")

        self.secQ_forgotpass = StringVar()

        self.bg_image = ImageTk.PhotoImage(
            file=r"C:\Users\divya\Desktop\Programming\DBMS Mini Project\bg_image.png")
        lblbg_image = Label(self.root, image=self.bg_image)
        lblbg_image.place(x=0, y=0)

        signinframe = Frame(self.root, bd=2, relief=RIDGE)
        signinframe.place(x=100, y=100, width=520, height=600)

        Label(signinframe, relief=RIDGE, bd=0, text="+ HOSPITAL MANAGEMENT SYSTEM +",
              fg="green", font=("open sans", 16, "bold")).place(x=64, y=30)

        Label(signinframe, relief=RIDGE, bd=0, text="Sign In",
              fg="Black", font=("open sans", 20)).place(x=215, y=80)

        Label(signinframe, relief=RIDGE, bd=0, text="Use only Authorised Account",
              fg="black", font=("open sans", 13)).place(x=150, y=120)

        Label(signinframe, font=(
            "open sans", 12), text="User ID:", padx=2, pady=6).place(x=50, y=170)

        self.txt_userid = ttk.Entry(signinframe, font=("open sans", 12))
        self.txt_userid.place(x=50, y=210, width=350, height=30)

        Label(signinframe, font=(
            "open sans", 12), text="Password:", padx=2, pady=6).place(x=50, y=280)

        self.txt_password = ttk.Entry(
            signinframe, font=("open sans", 12), show="*")
        self.txt_password.place(x=50, y=320, width=350, height=30)

        Button(signinframe, text="Forgot Password?", bd=0, command=self.forgotPass, font=(
            "open sans", 11)).place(x=50, y=370)

        Button(signinframe, text="Create Account", bd=1, command=self.signUpWindow,
               font=("open sans", 13,)).place(x=50, y=450)

        Button(signinframe, command=self.login_authenticate, text="Sign in", bd=1,
               font=("open sans", 13,)).place(x=335, y=450)

    def signUpWindow(self):
        """This function opens the signup window on top of login window"""
        self.new_window = Toplevel(self.root)
        self.app = SignUpPage(self.new_window)

    def login_authenticate(self):
        """This function redirects to the project once successfully logged in"""
        if (self.txt_userid.get() == "") or (self.txt_password.get() == ""):
            messagebox.showerror("Error", "All fields are required")
        elif (self.txt_userid.get() == "hmsadmin") and (self.txt_password.get() == "hmsadmin"):
            self.new_window = Toplevel()
            self.app = Hospital(self.new_window)
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Divyansh@256adv",
                database="hospitaldb"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM useraccounts WHERE userid=%s AND password=%s", (
                self.txt_userid.get(), self.txt_password.get()
            ))
            row = my_cursor.fetchone()
            if row == None:
                messagebox.showerror("Error", "Invalid Username/Password")
            else:
                self.new_window = Toplevel()
                self.app = Hospital(self.new_window)
            conn.commit()
            conn.close()

    def ConfirmButton(self):
        if self.secQ_forgotpass.get() == "Select":
            messagebox.showerror(
                "Error", "Select the Security Question first!", parent=self.root2)
        elif self.txt_security_ans.get() == "":
            messagebox.showerror(
                "Error", "Enter the Security Answer!", parent=self.root2)
        elif self.txt_newPass.get() == "":
            messagebox.showerror(
                "Error", "Enter the New Password!", parent=self.root2)
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Divyansh@256adv",
                database="hospitaldb"
            )
            my_cursor = conn.cursor()
            query = (
                "SELECT * FROM useraccounts WHERE userid=%s AND securityques=%s AND securityans=%s")
            value = (self.txt_userid.get(), self.secQ_forgotpass.get(),
                     self.txt_security_ans.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            if row == None:
                messagebox.showerror(
                    "Error", "Enter the correct Security Answer", parent=self.root2)
            else:
                query = ("UPDATE useraccounts SET password=%s WHERE userid=%s")
                value = (self.txt_newPass.get(), self.txt_userid.get(),)
                my_cursor.execute(query, value)

                conn.commit()
                conn.close()
                messagebox.showinfo(
                    "Success", "Reset Password Successful!", parent=self.root2)

    def SigninInstead(self):
        self.root2.destroy()

    def forgotPass(self):
        if self.txt_userid.get() == "":
            messagebox.showerror("Error", "User ID is empty!")
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Divyansh@256adv",
                database="hospitaldb"
            )
            my_cursor = conn.cursor()
            query = ("SELECT * FROM useraccounts WHERE userid=%s")
            value = (self.txt_userid.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            if row == None:
                messagebox.showerror("Error", "User ID doesn't exist!")
            else:
                conn.close()
                self.root2 = Toplevel()
                self.root2.title("Forgot Password")
                self.root2.geometry("520x600+100+100")

                Label(self.root2, relief=RIDGE, bd=0, text="+ HOSPITAL MANAGEMENT SYSTEM +",
                      fg="green", font=("open sans", 16, "bold")).place(x=64, y=30)

                Label(self.root2, relief=RIDGE, bd=0, text="Password Recovery",
                      fg="red", font=("open sans", 20)).place(x=140, y=70)

                Label(self.root2, relief=RIDGE, bd=0, text="(This helps show that this account really belongs to you)",
                      fg="Black", font=("open sans", 9)).place(x=105, y=110)

                Label(self.root2, relief=RIDGE, bd=1, text=self.txt_userid.get(),
                      fg="Black", font=("open sans", 15)).place(x=225, y=140)

                Label(self.root2, font=(
                    "open sans", 12), text="Select Security Question:", padx=2, pady=6).place(x=50, y=190)

                security_ques = ttk.Combobox(
                    self.root2, state="readonly", font=("open sans", 12), width=33, textvariable=self.secQ_forgotpass)
                security_ques["values"] = (
                    "Select", "What is your name", "Where do you live")
                security_ques.place(x=55, y=230, width=400, height=30)
                security_ques.current(0)

                Label(self.root2, font=(
                    "open sans", 12), text="Security Answer:", padx=2, pady=6).place(x=50, y=270)

                self.txt_security_ans = ttk.Entry(self.root2, font=(
                    "open sans", 12))
                self.txt_security_ans.place(x=55, y=310, width=400, height=30)

                Label(self.root2, font=(
                    "open sans", 12), text="New Password:", padx=2, pady=6).place(x=50, y=350)

                self.txt_newPass = ttk.Entry(self.root2, font=(
                    "open sans", 12))
                self.txt_newPass.place(x=55, y=390, width=400, height=30)

                Button(self.root2, text="Confirm", bd=1, bg="green", command=self.ConfirmButton,
                       font=("open sans", 13,), fg="white", activebackground="green").place(x=55, y=450)

                Button(self.root2, text="Sign in Instead", bd=1, bg="green", command=self.SigninInstead,
                       font=("open sans", 13,), fg="white", activebackground="green").place(x=333, y=450)


class SignUpPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1520x880+0+0")

        self.userid = StringVar()
        self.password = StringVar()
        self.securityques = StringVar()
        self.securityans = StringVar()

        self.bg_image = ImageTk.PhotoImage(
            file=r"C:\Users\divya\Desktop\Programming\DBMS Mini Project\bg_image.png")
        lblbg_image = Label(self.root, image=self.bg_image)
        lblbg_image.place(x=0, y=0)

        signupframe = Frame(self.root, bd=2, relief=RIDGE)
        signupframe.place(x=40, y=40, width=700, height=700)

        Label(signupframe, relief=RIDGE, bd=0, text="+ HOSPITAL MANAGEMENT SYSTEM +",
              fg="green", font=("open sans", 16, "bold")).place(x=20, y=20)

        Label(signupframe, relief=RIDGE, bd=0, text="Create a New Account",
              fg="red", font=("open sans", 20)).place(x=20, y=70)

        Label(signupframe, font=(
            "open sans", 12), text="User ID:", padx=2, pady=6).place(x=20, y=130)

        self.txt_userid = ttk.Entry(signupframe, font=(
            "open sans", 12), textvariable=self.userid)
        self.txt_userid.place(x=20, y=170, width=350, height=30)

        Label(signupframe, font=(
            "open sans", 12), text="Password:", padx=2, pady=6).place(x=20, y=210)

        self.txt_password = ttk.Entry(signupframe, font=(
            "open sans", 12), textvariable=self.password)
        self.txt_password.place(x=20, y=250, width=350, height=30)

        Label(signupframe, font=(
            "open sans", 12), text="Confirm Password:", padx=2, pady=6).place(x=20, y=290)

        self.txt_cnfpassword = ttk.Entry(signupframe, font=("open sans", 12))
        self.txt_cnfpassword.place(x=20, y=330, width=350, height=30)

        Label(signupframe, font=(
            "open sans", 12), text="Security Question:", padx=2, pady=6).place(x=20, y=370)

        Label(signupframe, font=(
            "open sans", 9), text="(In case you forget password)", padx=2, pady=6).place(x=20, y=400)

        security_ques = ttk.Combobox(
            signupframe, state="readonly", font=("open sans", 12), width=33, textvariable=self.securityques)
        security_ques["values"] = (
            "Select", "What is your name", "Where do you live")
        security_ques.place(x=20, y=430, width=350, height=30)
        security_ques.current(0)

        Label(signupframe, font=(
            "open sans", 12), text="Security Answer:", padx=2, pady=6).place(x=20, y=470)

        Label(signupframe, font=(
            "open sans", 9), text="(You will be asked to enter this answer if you forget password)", padx=2, pady=6).place(x=20, y=500)

        self.txt_security_ans = ttk.Entry(signupframe, font=(
            "open sans", 12), textvariable=self.securityans)
        self.txt_security_ans.place(x=20, y=540, width=350, height=30)

        Button(signupframe, text="Register", bd=1, command=self.registerData,
               font=("open sans", 13,)).place(x=20, y=600)

        Button(signupframe, text="Sign in Instead", bd=1, command=self.SigninInstead,
               font=("open sans", 13,)).place(x=248, y=600)

        self.createaccount_image = ImageTk.PhotoImage(
            file=r"C:\Users\divya\Desktop\Programming\DBMS Mini Project\createaccount.png")
        lblbg_image = Label(signupframe, image=self.createaccount_image)
        lblbg_image.place(x=500, y=200, width=100, height=93)

        Label(signupframe, relief=RIDGE, bd=0, text="One Account\nto access all database",
              fg="Black", font=("open sans", 13)).place(x=465, y=300)

    def registerData(self):
        if ((self.userid.get() == "") or (self.password.get() == "") or (self.securityques.get() == "Select") or (self.securityans.get() == "")):
            messagebox.showerror(
                "Error", "All fields are required", parent=self.root)
        elif (self.password.get() != self.txt_cnfpassword.get()):
            messagebox.showerror(
                "Error", "Password doesn't match!", parent=self.root)
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Divyansh@256adv",
                database="hospitaldb"
            )
            my_cursor = conn.cursor()
            query = ("SELECT * FROM useraccounts WHERE userid=%s")
            value = (self.userid.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            if row != None:
                messagebox.showerror(
                    "Error", "User already registered!", parent=self.root)
            else:
                my_cursor.executemany("INSERT INTO useraccounts VALUES (%s, %s, %s, %s)", [(self.userid.get(
                ), self.password.get(), self.securityques.get(), self.securityans.get())])
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User registered successfully!")

    def SigninInstead(self):
        self.root.destroy()


class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1520x880+0+0")

        self.NameOfTablet = StringVar()
        self.ReferenceNo = StringVar()
        self.Dose = StringVar()
        self.NoOfTablets = StringVar()
        self.Lot = StringVar()
        self.IssueDate = StringVar()
        self.ExpiryDate = StringVar()
        self.DailyDose = StringVar()
        self.SideEffect = StringVar()
        self.FurtherInfo = StringVar()
        self.BloodPressure = StringVar()
        self.Storage = StringVar()
        self.Medication = StringVar()
        self.PatientID = StringVar()
        self.NHSNumber = StringVar()
        self.PatientName = StringVar()
        self.DateOfBirth = StringVar()
        self.PatientAddress = StringVar()

        lbltitle = Label(self.root, bd=20, relief=RIDGE, text="+ HOSPITAL MANAGEMENT SYSTEM +",
                         fg="green", bg="white", font=("open sans", 45, "bold"))
        lbltitle.pack(side=TOP, fill=X)

        # -----------------Data Frame------------------

        Dataframe = Frame(self.root, bd=20, relief=RIDGE)
        Dataframe.place(x=0, y=100, width=1520, height=400)

        DataframeLeft = LabelFrame(Dataframe, bd=10, padx=20, relief=RIDGE, font=(
            "arial", 12, "bold"), text="Patient Information")
        DataframeLeft.place(x=0, y=5, width=980, height=350)

        DataframeRight = LabelFrame(Dataframe, bd=10, padx=20, relief=RIDGE, font=(
            "arial", 12, "bold"), text="Prescription")
        DataframeRight.place(x=985, y=5, width=495, height=350)

        # -----------------Buttons Frame------------------

        Buttonsframe = Frame(self.root, bd=20, relief=RIDGE)
        Buttonsframe.place(x=0, y=500, width=1520, height=80)

        # -----------------Details Frame------------------

        Detailsframe = Frame(self.root, bd=20, relief=RIDGE)
        Detailsframe.place(x=0, y=585, width=1520, height=200)

        # -----------------DataframeLeft------------------

        lblNameTablet = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Tablet Name:", padx=2, pady=6)
        lblNameTablet.grid(row=0, column=0, sticky=W)

        comNametablet = ttk.Combobox(
            DataframeLeft, textvariable=self.NameOfTablet, state="readonly", font=("open sans", 12, "bold"), width=33)
        comNametablet["values"] = ("Select", "Abacavir", "Bisoprolol", "Calamine", "Cefazolin", "Dacarbazine", "Isoflurane",
                                   "Morphine", "Plazomicin", "Retinol", "Salbutamol", "Triptorelin", "Yellow Fever Vaccine")
        comNametablet.current(0)
        comNametablet.grid(row=0, column=1)

        lblref = Label(DataframeLeft, font=("open sans", 12,
                       "bold"), text="Reference No.", padx=2)
        lblref.grid(row=1, column=0, sticky=W)
        txtref = Entry(DataframeLeft, textvariable=self.ReferenceNo,
                       font=("open sans", 12, "bold"), width=35)
        txtref.grid(row=1, column=1)

        lblDose = Label(DataframeLeft, font=("open sans", 12,
                        "bold"), text="Dose:", padx=2, pady=4)
        lblDose.grid(row=2, column=0, sticky=W)
        txtDose = Entry(DataframeLeft, textvariable=self.Dose, font=(
            "open sans", 12, "bold"), width=35)
        txtDose.grid(row=2, column=1)

        lblNoOfTablets = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="No. of Tablets:", padx=2, pady=6)
        lblNoOfTablets.grid(row=3, column=0, sticky=W)
        txtNoOfTablets = Entry(DataframeLeft, textvariable=self.NoOfTablets, font=(
            "open sans", 12, "bold"), width=35)
        txtNoOfTablets.grid(row=3, column=1)

        lblLot = Label(DataframeLeft, font=("open sans", 12,
                       "bold"), text="Lot:", padx=2, pady=6)
        lblLot.grid(row=4, column=0, sticky=W)
        txtLot = Entry(DataframeLeft, textvariable=self.Lot,
                       font=("open sans", 12, "bold"), width=35)
        txtLot.grid(row=4, column=1)

        lblIssueDate = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Issue Date:", padx=2, pady=6)
        lblIssueDate.grid(row=5, column=0, sticky=W)
        txtIssueDate = Entry(DataframeLeft, textvariable=self.IssueDate, font=(
            "open sans", 12, "bold"), width=35)
        txtIssueDate.grid(row=5, column=1)

        lblExpiryDate = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Expiry Date:", padx=2, pady=6)
        lblExpiryDate.grid(row=6, column=0, sticky=W)
        txtExpiryDate = Entry(DataframeLeft, textvariable=self.ExpiryDate, font=(
            "open sans", 12, "bold"), width=35)
        txtExpiryDate.grid(row=6, column=1)

        lblDailyDose = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Daily Dose:", padx=2, pady=4)
        lblDailyDose.grid(row=7, column=0, sticky=W)
        txtDailyDose = Entry(DataframeLeft, textvariable=self.DailyDose, font=(
            "open sans", 12, "bold"), width=35)
        txtDailyDose.grid(row=7, column=1)

        lblSideEffect = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Side Effect:", padx=2, pady=6)
        lblSideEffect.grid(row=8, column=0, sticky=W)
        txtSideEffect = Entry(DataframeLeft, textvariable=self.SideEffect, font=(
            "open sans", 12, "bold"), width=35)
        txtSideEffect.grid(row=8, column=1)

        lblFurtherInfo = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Further Info:", padx=2)
        lblFurtherInfo.grid(row=0, column=2, sticky=W)
        txtFurtherInfo = Entry(DataframeLeft, textvariable=self.FurtherInfo, font=(
            "open sans", 12, "bold"), width=35)
        txtFurtherInfo.grid(row=0, column=3)

        lblBloodPressure = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Blood Pressure:", padx=2, pady=6)
        lblBloodPressure.grid(row=1, column=2, sticky=W)
        txtBloodPressure = Entry(DataframeLeft, textvariable=self.BloodPressure, font=(
            "open sans", 12, "bold"), width=35)
        txtBloodPressure.grid(row=1, column=3)

        lblStorage = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Storage Advice:", padx=2, pady=6)
        lblStorage.grid(row=2, column=2, sticky=W)
        txtStorage = Entry(DataframeLeft, textvariable=self.Storage, font=(
            "open sans", 12, "bold"), width=35)
        txtStorage.grid(row=2, column=3)

        lblMedicine = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Medication:", padx=2, pady=6)
        lblMedicine.grid(row=3, column=2, sticky=W)
        txtMedicine = Entry(DataframeLeft, textvariable=self.Medication, font=(
            "open sans", 12, "bold"), width=35)
        txtMedicine.grid(row=3, column=3)

        lblPatientId = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Patient ID:", padx=2, pady=6)
        lblPatientId.grid(row=4, column=2, sticky=W)
        txtPatientId = Entry(DataframeLeft, textvariable=self.PatientID, font=(
            "open sans", 12, "bold"), width=35)
        txtPatientId.grid(row=4, column=3)

        lblNhsNumber = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="NHS Number:", padx=2, pady=6)
        lblNhsNumber.grid(row=5, column=2, sticky=W)
        txtNhsNumber = Entry(DataframeLeft, textvariable=self.NHSNumber, font=(
            "open sans", 12, "bold"), width=35)
        txtNhsNumber.grid(row=5, column=3)

        lblPatientName = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Patient Name:", padx=2, pady=6)
        lblPatientName.grid(row=6, column=2, sticky=W)
        txtPatientName = Entry(DataframeLeft, textvariable=self.PatientName, font=(
            "open sans", 12, "bold"), width=35)
        txtPatientName.grid(row=6, column=3)

        lblDateOfBirth = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Date of Birth:", padx=2, pady=6)
        lblDateOfBirth.grid(row=7, column=2, sticky=W)
        txtDateOfBirth = Entry(DataframeLeft, textvariable=self.DateOfBirth, font=(
            "open sans", 12, "bold"), width=35)
        txtDateOfBirth.grid(row=7, column=3)

        lblPatientAddress = Label(DataframeLeft, font=(
            "open sans", 12, "bold"), text="Patient Address:", padx=2, pady=6)
        lblPatientAddress.grid(row=8, column=2, sticky=W)
        txtPatientAddress = Entry(DataframeLeft, textvariable=self.PatientAddress, font=(
            "open sans", 12, "bold"), width=35)
        txtPatientAddress.grid(row=8, column=3)

        # -----------------DataframeRight------------------

        self.txtPrescription = Text(DataframeRight, font=(
            "open sans", 12, "bold"), width=49, height=16, padx=2, pady=6)
        self.txtPrescription.grid(row=0, column=0)

        # -----------------Buttons------------------

        buttonPrescription = Button(Buttonsframe, text="Prescription", command=self.PrescriptionButton, bg='maroon', fg='white', font=(
            "open sans", 12, "bold"), width=23, height=1, padx=2, pady=6)
        buttonPrescription.grid(row=0, column=0)

        buttonPrescriptionData = Button(Buttonsframe, text="Prescription Data", command=self.PrescriptionDataButton, bg='maroon', fg='white', font=(
            "open sans", 12, "bold"), width=23, height=1, padx=2, pady=6)
        buttonPrescriptionData.grid(row=0, column=1)

        buttonUpdate = Button(Buttonsframe, text="Update", command=self.UpdateButton, bg='maroon', fg='white', font=(
            "open sans", 12, "bold"), width=23, height=1, padx=2, pady=6)
        buttonUpdate.grid(row=0, column=2)

        buttonDelete = Button(Buttonsframe, text="Delete", command=self.DeleteButton, bg='maroon', fg='white', font=(
            "open sans", 12, "bold"), width=23, height=1, padx=2, pady=6)
        buttonDelete.grid(row=0, column=3)

        buttonClear = Button(Buttonsframe, text="Clear", command=self.ClearButton, bg='maroon', fg='white', font=(
            "open sans", 12, "bold"), width=23, height=1, padx=2, pady=6)
        buttonClear.grid(row=0, column=4)

        buttonLogout = Button(Buttonsframe, text="Logout", command=self.LogoutButton, bg='maroon', fg='white', font=(
            "open sans", 12, "bold"), width=23, height=1, padx=2, pady=6)
        buttonLogout.grid(row=0, column=5)

        # -----------------Scroll Bar------------------

        scroll_x = ttk.Scrollbar(Detailsframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Detailsframe, orient=VERTICAL)
        self.hospital_table = ttk.Treeview(Detailsframe, column=("Tablet Name", "Reference No.", "Dose", "No. of Tablets", "Lot", "Issue Date", "Expiry Date",
                                           "Daily Dose", "Side Effect", "Further Info", "Blood Pressure", "Storage", "Medication", "Patient ID", "NHS Number", "Patient Name", "Date of Birth", "Patient Address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.hospital_table.xview)
        scroll_y.config(command=self.hospital_table.yview)

        # -----------------Table------------------

        self.hospital_table.heading("Tablet Name", text="Tablet Name")
        self.hospital_table.heading("Reference No.", text="Reference No.")
        self.hospital_table.heading("Dose", text="Dose")
        self.hospital_table.heading("No. of Tablets", text="No. of Tablets")
        self.hospital_table.heading("Lot", text="Lot")
        self.hospital_table.heading("Issue Date", text="Issue Date")
        self.hospital_table.heading("Expiry Date", text="Expiry Date")
        self.hospital_table.heading("Daily Dose", text="Daily Dose")
        self.hospital_table.heading("Side Effect", text="Side Effect")
        self.hospital_table.heading("Further Info", text="Further Info")
        self.hospital_table.heading("Blood Pressure", text="Blood Pressure")
        self.hospital_table.heading("Storage", text="Storage")
        self.hospital_table.heading("Medication", text="Medication")
        self.hospital_table.heading("Patient ID", text="Patient ID")
        self.hospital_table.heading("NHS Number", text="NHS Number")
        self.hospital_table.heading("Patient Name", text="Patient Name")
        self.hospital_table.heading("Date of Birth", text="Date of Birth")
        self.hospital_table.heading("Patient Address", text="Patient Address")

        self.hospital_table["show"] = "headings"

        self.hospital_table.column("Tablet Name", width=100)
        self.hospital_table.column("Reference No.", width=100)
        self.hospital_table.column("Dose", width=100)
        self.hospital_table.column("No. of Tablets", width=100)
        self.hospital_table.column("Lot", width=100)
        self.hospital_table.column("Issue Date", width=100)
        self.hospital_table.column("Expiry Date", width=100)
        self.hospital_table.column("Daily Dose", width=100)
        self.hospital_table.column("Side Effect", width=100)
        self.hospital_table.column("Further Info", width=100)
        self.hospital_table.column("Blood Pressure", width=100)
        self.hospital_table.column("Storage", width=100)
        self.hospital_table.column("Medication", width=100)
        self.hospital_table.column("Patient ID", width=100)
        self.hospital_table.column("NHS Number", width=100)
        self.hospital_table.column("Patient Name", width=100)
        self.hospital_table.column("Date of Birth", width=100)
        self.hospital_table.column("Patient Address", width=100)

        self.hospital_table.pack(fill=BOTH, expand=1)
        self.hospital_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()

    # -----------------Button Functionality Declaration------------------
    def PrescriptionButton(self):
        self.txtPrescription.insert(
            END, "Tablet Name:\t\t\t" + self.NameOfTablet.get()+"\n")
        self.txtPrescription.insert(
            END, "Reference No:\t\t\t" + self.ReferenceNo.get()+"\n")
        self.txtPrescription.insert(END, "Dose:\t\t\t" + self.Dose.get()+"\n")
        self.txtPrescription.insert(
            END, "No. of Tablets:\t\t\t" + self.NoOfTablets.get()+"\n")
        self.txtPrescription.insert(END, "Lot:\t\t\t" + self.Lot.get()+"\n")
        self.txtPrescription.insert(
            END, "Issue Date:\t\t\t" + self.IssueDate.get()+"\n")
        self.txtPrescription.insert(
            END, "Expiry Date:\t\t\t" + self.ExpiryDate.get()+"\n")
        self.txtPrescription.insert(
            END, "Daily Dose:\t\t\t" + self.DailyDose.get()+"\n")
        self.txtPrescription.insert(
            END, "Side Effect:\t\t\t" + self.SideEffect.get()+"\n")
        self.txtPrescription.insert(
            END, "Further Info:\t\t\t" + self.FurtherInfo.get()+"\n")
        self.txtPrescription.insert(
            END, "Blood Pressure:\t\t\t" + self.BloodPressure.get()+"\n")
        self.txtPrescription.insert(
            END, "Storage:\t\t\t" + self.Storage.get()+"\n")
        self.txtPrescription.insert(
            END, "Medication:\t\t\t" + self.Medication.get()+"\n")
        self.txtPrescription.insert(
            END, "Patient ID:\t\t\t" + self.PatientID.get()+"\n")
        self.txtPrescription.insert(
            END, "NHS Number:\t\t\t" + self.NHSNumber.get()+"\n")
        self.txtPrescription.insert(
            END, "Patient Name:\t\t\t" + self.PatientName.get()+"\n")
        self.txtPrescription.insert(
            END, "Date of Birth:\t\t\t" + self.DateOfBirth.get()+"\n")
        self.txtPrescription.insert(
            END, "Patient Address:\t\t\t" + self.PatientAddress.get()+"\n")

    def PrescriptionDataButton(self):
        if self.NameOfTablet.get() == "" or self.ReferenceNo.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Divyansh@256adv",
                database="hospitaldb"
            )
            my_cursor = conn.cursor()
            my_cursor.executemany("INSERT INTO hospital VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [(
                self.NameOfTablet.get(),
                self.ReferenceNo.get(),
                self.Dose.get(),
                self.NoOfTablets.get(),
                self.Lot.get(),
                self.IssueDate.get(),
                self.ExpiryDate.get(),
                self.DailyDose.get(),
                self.SideEffect.get(),
                self.FurtherInfo.get(),
                self.BloodPressure.get(),
                self.Storage.get(),
                self.Medication.get(),
                self.PatientID.get(),
                self.NHSNumber.get(),
                self.PatientName.get(),
                self.DateOfBirth.get(),
                self.PatientAddress.get()
            )])
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Data Inserted Successfully")

    def UpdateButton(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Divyansh@256adv",
            database="hospitaldb"
        )
        my_cursor = conn.cursor()
        my_cursor.execute("UPDATE hospital set nameoftablet=%s, dose=%s, nooftablets=%s, lot=%s, issuedate=%s, expirydate=%s, dailydose=%s, sideeffect=%s, furtherinfo=%s, bloodpressure=%s, storage=%s, medication=%s, patientid=%s, nhsnumber=%s, patientname=%s, dob=%s, patientaddress=%s WHERE referenceno=%s", (
            self.NameOfTablet.get(),
            self.Dose.get(),
            self.NoOfTablets.get(),
            self.Lot.get(),
            self.IssueDate.get(),
            self.ExpiryDate.get(),
            self.DailyDose.get(),
            self.SideEffect.get(),
            self.FurtherInfo.get(),
            self.BloodPressure.get(),
            self.Storage.get(),
            self.Medication.get(),
            self.PatientID.get(),
            self.NHSNumber.get(),
            self.PatientName.get(),
            self.DateOfBirth.get(),
            self.PatientAddress.get(),
            self.ReferenceNo.get()
        ))
        conn.commit()
        self.fetch_data()
        conn.close()
        messagebox.showinfo("Update", "Data Updated Successfully")

    def DeleteButton(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Divyansh@256adv",
            database="hospitaldb"
        )
        my_cursor = conn.cursor()
        value = (self.ReferenceNo.get(),)
        my_cursor.execute(
            "DELETE FROM hospital WHERE referenceno=%s", value)
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Delete", "Data Deleted Successfully")

    def ClearButton(self):
        self.NameOfTablet.set("")
        self.ReferenceNo.set("")
        self.Dose.set("")
        self.NoOfTablets.set("")
        self.Lot.set("")
        self.IssueDate.set("")
        self.ExpiryDate.set("")
        self.DailyDose.set("")
        self.SideEffect.set("")
        self.FurtherInfo.set("")
        self.BloodPressure.set("")
        self.Storage.set("")
        self.Medication.set("")
        self.PatientID.set("")
        self.NHSNumber.set("")
        self.PatientName.set("")
        self.DateOfBirth.set("")
        self.PatientAddress.set("")
        self.txtPrescription.delete("1.0", END)

    def LogoutButton(self):
        logoutStatus = messagebox.askyesno(
            "Hospital Management System", "Confirm Logout?", parent=self.root)
        if (logoutStatus == 1):
            self.root.destroy()

    def fetch_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Divyansh@256adv",
            database="hospitaldb"
        )
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM hospital")
        rows = my_cursor.fetchall()
        if len(rows) != 0:
            self.hospital_table.delete(*self.hospital_table.get_children())
            for i in rows:
                self.hospital_table.insert("", END, values=i)
            conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.hospital_table.focus()
        content = self.hospital_table.item(cursor_row)
        value = content["values"]
        self.NameOfTablet.set(value[0])
        self.ReferenceNo.set(value[1])
        self.Dose.set(value[2])
        self.NoOfTablets.set(value[3])
        self.Lot.set(value[4])
        self.IssueDate.set(value[5])
        self.ExpiryDate.set(value[6])
        self.DailyDose.set(value[7])
        self.SideEffect.set(value[8])
        self.FurtherInfo.set(value[9])
        self.BloodPressure.set(value[10])
        self.Storage.set(value[11])
        self.Medication.set(value[12])
        self.PatientID.set(value[13])
        self.NHSNumber.set(value[14])
        self.PatientName.set(value[15])
        self.DateOfBirth.set(value[16])
        self.PatientAddress.set(value[17])


if __name__ == "__main__":
    startpgm()
