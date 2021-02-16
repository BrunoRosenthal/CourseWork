import sqlite3


def quiz(quiz, user):
    with sqlite3.connect("quiz.db")as db:
        cursor = db.cursor()

    score = 0
    cursor.execute("SELECT * FROM questions WHERE quizID=?;", [(quiz)])
    questions = cursor.fetchall()
    numQu = 0

    for question in questions:
        topic = question[1]
        print("What is the value of "  + question[2])
        print("\n 1. %s \n 2. %s \n 3. %s \n 4. %s \n" %(question[3], question[4], question[5], question[6]))
        choice = input("Which of these is the answer? ")
        if choice == question[7]:
            print("Correct")
            score += 1
            print("")
        else:
            print("Incorrect")
        numQu +=1
    print("You have finished this quiz")

    scorePercent = int((score/numQu)*100)
    print("You scored %s percent" %scorePercent)

    insertData = ("INSERT INTO scores(userID, score, quizID) VALUES(?,?,?);")
    cursor.execute(insertData, [(user), (scorePercent), (quiz)])
    db.commit()

