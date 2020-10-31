import sqlite3

# creating the database for the quiz if it doesn't already exist

with sqlite3.connect("quiz.db")as db:
    cursor = db.cursor()

# creating the table for users if it doesn't already exist

cursor.execute("""
CREATE TABLE IF NOT EXISTS user(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
Fname VARCHAR(20) NOT NULL,
Lname VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL);
""")

# creating table for the individual quizzes

cursor.execute("""
CREATE TABLE IF NOT EXISTS quizzes(
quizID INTEGER PRIMARY KEY,
quizName VARCHAR(20) NOT NULL);
""")

# creating the table for the scores

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores(
scoreID INTEGER PRIMARY KEY,
userID INTEGER NOT NULL,
score INTEGER NOT NULL,
quizID INTEGER NOT NULL,
FOREIGN KEY(userID) REFERENCES user(userID),
FOREIGN KEY(quizID) REFERENCES quizzes(quizID));
""")

# creating a table for the questions

cursor.execute("""
CREATE TABLE IF NOT EXISTS questions(
questionID INTEGER PRIMARY KEY,
quizID INTEGER NOT NULL,
question VARCHAR(100) NOT NULL,
option1 VARCHAR(50) NOT NULL,
option2 VARCHAR(50) NOT NULL,
option3 VARCHAR(50),
option4 VARCHAR(50),
answer VARCHAR(50),
FOREIGN KEY(quizID) REFERENCES quizzes(quizID));
""")

# TESTING CODE IS ALL BELOW:

# to delete all records

# cursor.execute("""DELETE FROM questions""")
# db.commit()

# to print all records

# cursor.execute("SELECT * FROM user")
# print(cursor.fetchall())

# to create test users

# cursor.execute(""" INSERT INTO user(username,Fname,Lname,password)
# VALUES("John2003","John","Smith","guest")""")
# db.commit()

# to show all tables

# tables = cursor.execute("""
# SELECT name FROM sqlite_master
# WHERE type="table"
# ORDER BY name;
# """)
# print(cursor.fetchall())
