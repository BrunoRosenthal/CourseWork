import sqlite3
import matplotlib.pyplot as plt

with sqlite3.connect("quiz.db")as db:
    cursor = db.cursor()

def showScores(user):
    query = ("""SELECT quiz.quizName, scores.score, user.userID
    FROM user INNER JOIN (quizzesd INNER JOIN scores ON quizzes.quizID = scores.quizID) ON user.userID = scores.userID
    WHERE (((user.userID)=?));""")
    cursor.execute(query, [(user)])
    results = cursor.fetchall()
    for line in results:
        print(line[0], str(line[1]) + "%")

def graph():
    y = []
    xaxis = []

    query = ("""SELECT quizzes.quizName, scores.score, user.userID
    FROM user INNER JOIN (quizzes INNER JOIN scores ON qizzes.quizID = scores.quizID) IN user.userID = scores.userID
    WHERE (((user.userID)=?));""")

    cursor.execute(query, [(1)])
    results.fetchall()
    for line in results:
        y.append(line[1])
        xaxis.append(line[0])

    x = [i for i in range(len(y))]
    plt.xticks(x, xaxis)
    plt.bar(x, y)
    plt.show()

