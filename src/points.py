import sqlite3


def init_db(file="users.db"):
    global con
    con = sqlite3.connect(file)

    con.executescript(
        """
CREATE TABLE IF NOT EXISTS "Classes" (
	"class_id"	INTEGER UNIQUE,
	"user_id"	INTEGER,
	PRIMARY KEY("class_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Students" (
	"name"	TEXT,
	"class_id"	INTEGER,
	"points"	INTEGER
);
"""
    )


def get_student_points(user, cl, name):
    pass


def set_student_points(user, cl, name, n):
    pass
