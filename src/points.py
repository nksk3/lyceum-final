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
CREATE TRIGGER IF NOT EXISTS check_duplicate_classes
BEFORE INSERT ON Classes
BEGIN
  SELECT RAISE(ABORT, "Duplicate classes")
  WHERE EXISTS(SELECT * FROM Classes
               WHERE user_id = NEW.user_id AND name = NEW.name);
END;
CREATE TRIGGER IF NOT EXISTS check_duplicate_studnets
BEFORE INSERT ON Students
BEGIN
  SELECT RAISE(ABORT, "Duplicate students")
  WHERE EXISTS(SELECT * FROM Students
               WHERE class_id = NEW.class_id AND name = NEW.name);
END;
"""
    )


def add_class(uid, name):
    con.execute("INSERT INTO Classes (user_id, name) VALUES(?, ?)", (uid, name))
    con.commit()


def add_student(cl, name):
    con.execute("INSERT INTO Students (class_id, name, points) VALUES(?, ?, 0)", (cl, name))
    con.commit()


def remove_class(uid, cl):
    con.execute("DELETE FROM Classes WHERE user_id = ? AND name = ?", (uid, cl))
    con.commit()


def remove_student(cl, name):
    con.execute("DELETE FROM Students WHERE class_id = ? AND name = ?", (cl, name))
    con.commit()


def get_classes(uid):
    return con.execute(
        "SELECT class_id, name FROM Classes WHERE user_id = ?", (uid,)
    ).fetchall()


def get_students(cl):
    return con.execute(
        "SELECT name, points FROM Students WHERE class_id = ?", (cl,)
    ).fetchall()


def set_student_points(cl, name, n):
    con.execute("UPDATE Students SET points = ? WHERE class_id = ? AND name = ?", (n, cl, name))
    con.commit()
