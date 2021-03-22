import tkinter as tk
import sqlite3
import time


# noinspection PyAttributeOutsideInit
class Gui(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master
        master.title("Quiz Game")
        master.resizable(0, 0)

        self.score = 0

        self.frame = tk.Frame(self.master)
        self.frame.grid()

    def clearFrame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def startMenu(self):
        self.clearFrame()

        createAccountBtn = tk.Button(self.master, text='Create account', command=lambda: self.createAccount())
        createAccountBtn.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        loginBtn = tk.Button(self.master, text='Login', command=lambda: self.login())
        loginBtn.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        quitBtn = tk.Button(self.master, text="Quit", command=self.master.destroy)
        quitBtn.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def createAccount(self):
        self.clearFrame()

        nameLabel = tk.Label(self.master, text='Name:')
        nameLabel.grid(row=0, column=0, padx=10, pady=10)

        self.nameBox = tk.Entry(self.master)
        self.nameBox.grid(row=0, column=1, padx=10, pady=10)

        surnameLabel = tk.Label(self.master, text='Surame:')
        surnameLabel.grid(row=1, column=0, padx=10, pady=10)

        self.surnameBox = tk.Entry(self.master)
        self.surnameBox.grid(row=1, column=1, padx=10, pady=10)

        usernameLabel = tk.Label(self.master, text='Username:')
        usernameLabel.grid(row=2, column=0, padx=10, pady=10)

        self.usernameBox = tk.Entry(self.master)
        self.usernameBox.grid(row=2, column=1, padx=10, pady=10)

        passwordLabel = tk.Label(self.master, text='Password:')
        passwordLabel.grid(row=3, column=0, padx=10, pady=10)

        self.passwordBox = tk.Entry(self.master)
        self.passwordBox.grid(row=3, column=1, padx=10, pady=10)

        confirmPasswordLabel = tk.Label(self.master, text='Confirm password:')
        confirmPasswordLabel.grid(row=4, column=0, padx=10, pady=10)

        self.confirmPasswordBox = tk.Entry(self.master)
        self.confirmPasswordBox.grid(row=4, column=1, padx=10, pady=10)

        backBtn = tk.Button(self.master, text="Back", command=lambda: self.startMenu())
        backBtn.grid(row=5, column=0, columnspan=1, padx=10, pady=10)

        enterBtn = tk.Button(self.master, text="Enter", command=lambda: self.getCreateInputs())
        enterBtn.grid(row=5, column=1, columnspan=1, padx=10, pady=10)

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

            created = tk.Label(self.master, text='Your account has been successfully created')
            created.grid(row=0, column=0)

            ok = tk.Button(self.master, text='ok', command=lambda: self.mainMenu())
            ok.grid(row=1, column=0)

        else:
            problems = ', '.join(errors)

            self.clearFrame()

            passwordLenError = tk.Label(self.master, text='Your account was not created because '+problems)
            passwordLenError.grid(row=0, column=0)

            ok = tk.Button(self.master, text='ok', command=lambda: self.createAccount())
            ok.grid(row=1, column=0)

    def login(self):
        self.clearFrame()

        usernameLabel = tk.Label(self.master, text='Username:')
        usernameLabel.grid(row=0, column=0, padx=10, pady=10)

        self.usernameBox = tk.Entry(self.master)
        self.usernameBox.grid(row=0, column=1, padx=10, pady=10)

        passwordLabel = tk.Label(self.master, text='Password:')
        passwordLabel.grid(row=1, column=0, padx=10, pady=10)

        self.passwordBox = tk.Entry(self.master)
        self.passwordBox.grid(row=1, column=1, padx=10, pady=10)

        backBtn = tk.Button(self.master, text="Back", command=lambda: self.startMenu())
        backBtn.grid(row=2, column=0, columnspan=1, padx=10, pady=10)

        enterBtn = tk.Button(self.master, text="Enter", command=lambda: self.getLoginInputs())
        enterBtn.grid(row=2, column=1, columnspan=1, padx=10, pady=10)

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

            welcomeMessage = tk.Label(self.master, text="Welcome "+self.username)
            welcomeMessage.grid(row=0, column=0)

            ok = tk.Button(self.master, text='ok', command=lambda: self.mainMenu())
            ok.grid(row=1, column=0)

        else:
            self.clearFrame()

            wrongMessage = tk.Label(self.master, text="Your username or password are incorrect.")
            wrongMessage.grid(row=0, column=0)

            ok = tk.Button(self.master, text='ok', command=lambda: self.login())
            ok.grid(row=1, column=0)

    def mainMenu(self):
        self.clearFrame()

        quizzesLabel = tk.Label(self.master, text="Quizzes:")
        quizzesLabel.grid(row=0, column=0, padx=10, pady=10)

        additionBtn = tk.Button(self.master, text="addition", command=lambda: self.quizChoice("1", "1"))
        additionBtn.grid(row=0, column=1, padx=10, pady=10)

        subtractionBtn = tk.Button(self.master, text="subtraction", command=lambda: self.quizChoice("2", "1"))
        subtractionBtn.grid(row=0, column=2, padx=10, pady=10)

        multiplicationBtn = tk.Button(self.master, text="multiplication", command=lambda: self.quizChoice("3", "1"))
        multiplicationBtn.grid(row=0, column=3, padx=10, pady=10)

        divisionBtn = tk.Button(self.master, text="division", command=lambda: self.quizChoice("4", "1"))
        divisionBtn.grid(row=0, column=4, padx=10, pady=10)

        toolsLabel = tk.Label(self.master, text="Tools:")
        toolsLabel.grid(row=1, column=0, padx=10, pady=10)

        scoresBtn = tk.Button(self.master, text="previous Scores")
        scoresBtn.grid(row=1, column=1, padx=10, pady=10)

        logoutBtn = tk.Button(self.master, text="logout", command=lambda: self.startMenu())
        logoutBtn.grid(row=1, column=2, padx=10, pady=10)

        switchBtn = tk.Button(self.master, text="switch account", command=lambda: self.login())
        switchBtn.grid(row=1, column=3, padx=10, pady=10)

        quitBtn = tk.Button(self.master, text="quit", command=lambda: self.master.destroy)
        quitBtn.grid(row=1, column=4, padx=10, pady=10)

    def correct(self, quiz, question):
        self.score += 1
        question = str(int(question) + 1)

        self.clearFrame()

        self.congrats = tk.Label(self.master, text="Correct")
        self.congrats.grid(row=0, column=0)

        self.ok = tk.Button(self.master, text='ok', command=lambda: self.quizChoice(quiz, question))
        self.ok.grid(row=1, column=0)

    def incorrect(self, quiz, question):
        question = str(int(question) + 1)

        self.failure = tk.Label(self.master, text="Incorrect")
        self.failure.grid(row=0, column=0)

        self.ok = tk.Button(self.master, text='ok', command=lambda: self.quizChoice(quiz, question))
        self.ok.grid(row=1, column=0)

    def checker(self, quiz, question, prevAns, prevCorrect):
        self.clearFrame()

        if prevAns == prevCorrect:
            self.correct(quiz, question)

        else:
            self.incorrect(quiz, question)


    def finished(self, quiz):

        self.clearFrame()

        scorePercent = int((self.score / 3) * 100)

        with sqlite3.connect("quiz.db")as db:
            cursor = db.cursor()

        check = "SELECT * FROM user WHERE username = ?"
        cursor.execute(check, [self.username])

        self.userID = check[0]

        insertData = "INSERT INTO scores(userID, score, quizID) VALUES(?,?,?);"
        cursor.execute(insertData, [self.userID, scorePercent, quiz])
        db.commit()

        self.clearFrame()

        self.finish = tk.Label(self.master, text="You have finished the quiz")
        self.finish.grid(row=0, column=0)

        self.scored = tk.Label(self.master, text=("You scored %s percent" % scorePercent))
        self.scored.grid(row=1, column=0)

        self.ok = tk.Button(self.master, text='ok', command=lambda: self.mainMenu())
        self.ok.grid(row=2, column=0)

    def quizChoice(self, quiz, question):

        self.clearFrame()

        #print(self.score)

        if question == "0":
            self.score = 0

        if question == "4":
            self.finished(quiz)


        else:

            with sqlite3.connect("quiz.db")as db:
                cursor = db.cursor()

            cursor.execute("SELECT * FROM questions WHERE quizID=? AND questionID=?;", [quiz, question])
            q = cursor.fetchall()
            print(q)
            questions = q[0]
            print(quiz)


            self.questionLabel = tk.Label(self.master, text="what is the value of "+questions[2])
            self.questionLabel.grid(row=0, column=0)

            self.ansBtn1 = tk.Label(self.master, text=questions[3])
            self.ansBtn1.grid(row=1, column=0)

            self.ansBtn2 = tk.Label(self.master, text=questions[4])
            self.ansBtn2.grid(row=1, column=1)

            self.ansBtn3 = tk.Label(self.master, text=questions[5])
            self.ansBtn3.grid(row=2, column=0)

            self.ansBtn4 = tk.Label(self.master, text=questions[6])
            self.ansBtn4.grid(row=2, column=1)

            self.text = tk.Label(self.master, text="Enter your answer here:")
            self.text.grid(row=3, column=0)

            self.entry = tk.Entry(self.master)
            self.entry.grid(row=3, column=1)

            self.ok = tk.Button(self.master, text="Submit answer", command=lambda: self.checker(quiz, question, self.entry.get(), questions[7]))
            self.ok.grid(row=4, column=0, columnspan=2)





root = tk.Tk()
G = Gui(root)
G.startMenu()
root.mainloop()

