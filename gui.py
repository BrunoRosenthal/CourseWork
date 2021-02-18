import tkinter as tk
import sqlite3


# noinspection PyAttributeOutsideInit
class Gui(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master
        master.title("Quiz Game")
        master.resizable(0, 0)

        self.frame = tk.Frame(self.master)
        self.frame.grid()

    def clearFrame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def startMenu(self):
        self.clearFrame()

        self.createAccountBtn = tk.Button(self.master, text='Create account', command=lambda: self.createAccount())
        self.createAccountBtn.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.loginBtn = tk.Button(self.master, text='Login', command=lambda: self.login())
        self.loginBtn.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.quitBtn = tk.Button(self.master, text="Quit", command=self.master.destroy)
        self.quitBtn.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def createAccount(self):
        self.clearFrame()

        self.nameLabel = tk.Label(self.master, text='Name:')
        self.nameLabel.grid(row=0, column=0, padx=10, pady=10)

        self.nameBox = tk.Entry(self.master)
        self.nameBox.grid(row=0, column=1, padx=10, pady=10)

        self.surnameLabel = tk.Label(self.master, text='Surame:')
        self.surnameLabel.grid(row=1, column=0, padx=10, pady=10)

        self.surnameBox = tk.Entry(self.master)
        self.surnameBox.grid(row=1, column=1, padx=10, pady=10)

        self.usernameLabel = tk.Label(self.master, text='Username:')
        self.usernameLabel.grid(row=2, column=0, padx=10, pady=10)

        self.usernameBox = tk.Entry(self.master)
        self.usernameBox.grid(row=2, column=1, padx=10, pady=10)

        self.passwordLabel = tk.Label(self.master, text='Password:')
        self.passwordLabel.grid(row=3, column=0, padx=10, pady=10)

        self.passwordBox = tk.Entry(self.master)
        self.passwordBox.grid(row=3, column=1, padx=10, pady=10)

        self.confirmPasswordLabel = tk.Label(self.master, text='Confirm password:')
        self.confirmPasswordLabel.grid(row=4, column=0, padx=10, pady=10)

        self.confirmPasswordBox = tk.Entry(self.master)
        self.confirmPasswordBox.grid(row=4, column=1, padx=10, pady=10)

        self.backBtn = tk.Button(self.master, text="Back", command=lambda: self.startMenu())
        self.backBtn.grid(row=5, column=0, columnspan=1, padx=10, pady=10)

        self.enterBtn = tk.Button(self.master, text="Enter", command=lambda: self.getCreateInputs())
        self.enterBtn.grid(row=5, column=1, columnspan=1, padx=10, pady=10)

    def getCreateInputs(self):
        self.fname = self.nameBox.get()
        self.lname = self.surnameBox.get()
        self.username = self.usernameBox.get()
        self.password1 = self.passwordBox.get()
        self.password2 = self.confirmPasswordBox.get()
        self.clearFrame()
        self.new_user()

    def new_user(self):

        errors = []
        #  checking username isn't already in use

        with sqlite3.connect("quiz.db")as db:
            cursor = db.cursor()
        clash = "SELECT * FROM user WHERE username = ?"

        # using ? to prevent sql injection, hence making database more secure

        cursor.execute(clash, [self.username])
        x = cursor.fetchall()
        if x:
            errors.append("username is in use")

        if self.password1 != self.password2:
            errors.append("unmatched passwords")

        if len(self.password1) < 8:
            errors.append("password must be 8 characters long")

        if not errors:

            self.password = self.password1

            add_user = "INSERT INTO user(username, Fname, Lname, password) values(?,?,?,?)"
            cursor.execute(add_user, [self.username, self.fname, self.lname, self.password])
            db.commit()

            self.clearFrame()

            self.created = tk.Label(self.master, text='Your account has been successfully created')
            self.created.grid(row=0, column=0)

            self.ok = tk.Button(self.master, text='ok', command=lambda: self.mainMenu())
            self.ok.grid(row=1, column=0)

        else:
            problems = ', '.join(errors)

            self.clearFrame()

            self.passwordLenError = tk.Label(self.master, text='Your account was not created because '+problems)
            self.passwordLenError.grid(row=0, column=0)

            self.ok = tk.Button(self.master, text='ok', command=lambda: self.createAccount())
            self.ok.grid(row=1, column=0)

    def login(self):
        self.clearFrame()

        self.usernameLabel = tk.Label(self.master, text='Username:')
        self.usernameLabel.grid(row=0, column=0, padx=10, pady=10)

        self.usernameBox = tk.Entry(self.master)
        self.usernameBox.grid(row=0, column=1, padx=10, pady=10)

        self.passwordLabel = tk.Label(self.master, text='Password:')
        self.passwordLabel.grid(row=1, column=0, padx=10, pady=10)

        self.passwordBox = tk.Entry(self.master)
        self.passwordBox.grid(row=1, column=1, padx=10, pady=10)

        self.backBtn = tk.Button(self.master, text="Back", command=lambda: self.startMenu())
        self.backBtn.grid(row=2, column=0, columnspan=1, padx=10, pady=10)

        self.enterBtn = tk.Button(self.master, text="Enter", command=lambda: self.getLoginInputs())
        self.enterBtn.grid(row=2, column=1, columnspan=1, padx=10, pady=10)

    def getLoginInputs(self):
        self.username = self.usernameBox.get()
        self.password = self.passwordBox.get()
        self.user_login()

    def user_login(self):
        with sqlite3.connect("quiz.db")as db:
            cursor = db.cursor()
        check = "SELECT * FROM user WHERE username = ? AND password = ?"
        cursor.execute(check, [self.username, self.password])
        valid_user = cursor.fetchall()

        if valid_user:
            self.clearFrame()

            self.welcomeMessage = tk.Label(self.master, text="Welcome "+self.username)
            self.welcomeMessage.grid(row=0, column=0)

            self.ok = tk.Button(self.master, text='ok', command=lambda: self.mainMenu())
            self.ok.grid(row=1, column=0)

        else:
            self.clearFrame()

            self.wrongMessage = tk.Label(self.master, text="Your username or password are incorrect.")
            self.wrongMessage.grid(row=0, column=0)

            self.ok = tk.Button(self.master, text='ok', command=lambda: self.login())
            self.ok.grid(row=1, column=0)

    def mainMenu(self):
        self.clearFrame()

        self.quizzesLabel = tk.Label(self.master, text="Quizzes:")
        self.quizzesLabel.grid(row=0, column=0, padx=10, pady=10)

        self.additionBtn = tk.Button(self.master, text="addition", command=lambda: self.quizChoice("1"))
        self.additionBtn.grid(row=0, column=1, padx=10, pady=10)

        self.subtractionBtn = tk.Button(self.master, text="subtraction", command=lambda: self.quizChoice("2"))
        self.subtractionBtn.grid(row=0, column=2, padx=10, pady=10)

        self.multiplicationBtn = tk.Button(self.master, text="multiplication",
                                           command=lambda: self.quizChoice("3"))
        self.multiplicationBtn.grid(row=0, column=3, padx=10, pady=10)

        self.divisionBtn = tk.Button(self.master, text="division", command=lambda: self.quizChoice("4"))
        self.divisionBtn.grid(row=0, column=4, padx=10, pady=10)

        self.toolsLabel = tk.Label(self.master, text="Tools:")
        self.toolsLabel.grid(row=1, column=0, padx=10, pady=10)

        self.scoresBtn = tk.Button(self.master, text="previous Scores")
        self.scoresBtn.grid(row=1, column=1, padx=10, pady=10)

        self.logoutBtn = tk.Button(self.master, text="logout", command=lambda: self.startMenu())
        self.logoutBtn.grid(row=1, column=2, padx=10, pady=10)

        self.switchBtn = tk.Button(self.master, text="switch account", command=lambda: self.login())
        self.switchBtn.grid(row=1, column=3, padx=10, pady=10)

        self.quitBtn = tk.Button(self.master, text="quit", command=self.master.destroy)
        self.quitBtn.grid(row=1, column=4, padx=10, pady=10)

    def quizChoice(self, quiz):
        self.clearFrame()

        with sqlite3.connect("quiz.db")as db:
            cursor = db.cursor()

        score = 0
        cursor.execute("SELECT * FROM questions WHERE quizID=?;", [quiz])
        questions = cursor.fetchall()
        numQu = 0

        for question in questions:

            self.questionLabel = tk.Label(self.master, text=question[2])
            self.questionLabel.grid(row=0, column=0)

            self.ansBtn1 = tk.Button(self.master, text=question[3], command=(lambda: self.choice=question[3]))
            self.ansBtn1.grid(row=1, column=0)

            self.ansBtn2 = tk.Button(self.master, text=question[4], command=(lambda: self.choice=question[4]))
            self.ansBtn2.grid(row=1, column=1)

            self.ansBtn3 = tk.Button(self.master, text=question[5], command=(lambda: self.choice=question[5]))
            self.ansBtn3.grid(row=2, column=0)

            self.ansBtn4 = tk.Button(self.master, text=question[6], command=(lambda: self.choice=question[6]))
            self.ansBtn4.grid(row=2, column=1)

            if self.choice == question[7]:
                self.clearFrame()

                self.congrats = tk.Label(self.master, text="Correct")
                self.congrats.pack(row=0, column=0)

                self.ok = tk.Button(self.master, text='ok')
                self.ok.pack(row=1, column=0)

                score += 1

            else:
                self.clearFrame()

                self.failure = tk.Label(self.master, text="Incorrect")
                self.failure.pack(row=0, column=0)

                self.ok = tk.Button(self.master, text='ok')
                self.ok.pack(row=1, column=0)
            numQu += 1

        scorePercent = int((score / numQu) * 100)

        insertData = "INSERT INTO scores(userID, score, quizID) VALUES(?,?,?);"
        cursor.execute(insertData, [self.user, scorePercent, quiz])
        db.commit()

        self.clearFrame()

        self.finish = tk.Label(self.master, text="You have finished the quiz")
        self.finish.pack(row=0, column=0)

        self.scored = tk.Label(self.master, text=("You scored %s percent" % scorePercent))
        self.scored.pack(row=1, column=0)

        self.ok = tk.Button(self.master, text='ok', command=self.mainMenu())
        self.ok.pack(row=2, column=0)


root = tk.Tk()
G = Gui(root)
G.startMenu()
root.mainloop()
