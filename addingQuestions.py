import sqlite3

with sqlite3.connect("quiz.db")as db:
    cursor = db.cursor()

cursor.execute("""DELETE FROM quizzes""")
db.commit()

cursor.execute("""
INSERT INTO quizzes(quizName)
VALUES("Addition"),("Subtraction"),("Multiplication"),("Division"),("Advanced arithmetic");
""")
db.commit()

cursor.execute("""DELETE FROM questions""")
db.commit()

cursor.execute("""
INSERT INTO questions(quizID,question,option1,option2,option3,option4,answer)
VALUES("1","2+2","4","5","6","7","1"),
("1","2+3","4","5","6","7","2"),
("1","3+4","4","5","6","7","4"),

("2","2-1","1","5","6","7","1"),
("2","3-2","1","5","6","7","1"),
("2","3-1","2","5","6","7","1"),

("3","2x1","2","5","6","7","1"),
("3","3x2","1","3","6","7","3"),
("3","3x1","2","3","6","7","2"),

("3","2x1","2","5","6","7","1"),
("3","3x2","1","3","6","7","3"),
("3","3x1","2","3","6","7","2"),

("4","2/1","2","5","6","7","1"),
("4","6/2","1","3","6","7","2"),
("4","3/1","2","3","6","7","2"),

("5","2^1","2","5","6","7","1"),
("5","6^2","1","3","6","36","4"),
("5","9^(1/2)","2","3","6","7","1");
""")
db.commit()



