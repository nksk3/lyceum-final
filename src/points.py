import sqlite3


def init_db(file="data.db"):
    global con
    con = sqlite3.connect(file, check_same_thread=False)

    con.executescript(
        """
CREATE TABLE IF NOT EXISTS "Classes" (
"class_id" INTEGER UNIQUE,
"user_id" INTEGER,
"name" TEXT,
PRIMARY KEY("class_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Students" (
"name" TEXT,
"class_id" INTEGER,
"points" INTEGER
);
CREATE TRIGGER IF NOT EXISTS check_duplicate_studnets
BEFORE INSERT ON Students
BEGIN
  SELECT RAISE(ABORT, "Duplicate student")
  WHERE EXISTS(SELECT * FROM Students
               WHERE class_id = NEW.class_id AND name = NEW.name);
END;
"""
    )


def add_class(uid, name):
    con.execute(
        "INSERT INTO Classes (user_id, name) VALUES(?, ?)", (uid, name)
    )


def add_student(cl, name):
    con.execute(
        "INSERT INTO Students (name, class_id) VALUES(?, ?)", (cl, name)
    )


def get_classes(uid):
    return con.execute(
        "SELECT class_id, name FROM Classes WHERE user_id = ?", (uid,)
    ).fetchall()


def get_student_names(cl):
    return con.execute("SELECT name FROM Students WHERE class_id = ?", (cl,))


def get_student_points(cl, name):
    return con.execute(
        "SELECT points FROM Students WHERE class_id = ? AND name = ?",
        (cl, name),
    ).fetchone()[0]


def set_student_points(cl, name, n):
    pass
