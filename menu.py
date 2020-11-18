import login
import quiz
import analytics
import sqlite3

# next function gives menu for logged in users

def logged_in(user):
    with sqlite3.connect("quiz.db")as db:
        cursor = db.cursor()

    cursor.execute("SELECT * FROM quizzes;")
    results = (cursor.fetchall())

    # adding the different menu options for all inserted quizzes

    quizzes_menu = []
    for i in results:
        quizzes_menu.append(i[1])
    quizzes_menu.append("Show past scores")
    quizzes_menu.append("Graph of past scores")
    quizzes_menu.append("Exit")

    while True:
        option = 1
        for item in quizzes_menu:
            print(option, "-", item)
            option += 1

        userChoice = input("What quiz/analytics tool do you want? ")
        choices = len(quizzes_menu) - 3


        if userChoice == str(choices + 1):
            analytics.showScores(user)

        elif userChoice == str(choices + 2):
            analytics.graph(user)

        elif userChoice == str(choices + 3):
            break

        elif int(userChoice) <= choices:
            quiz.quiz(userChoice,user)



while True:
    choice = int(input("""
    Please choose from the following:
    
    1 - Create account
    2 - Login to existing account
    3 - Exit
    
    """))

    if choice == 1:
        login.new_user()

    if choice == 2:
        go = login.user_login()
        if go[0] != "N":
            logged_in(go[1])
        else:
            break

    if choice == 3:
        break

    elif choice not in[1, 2, 3]:
        print("please choose a number between 1 and 3 ")
