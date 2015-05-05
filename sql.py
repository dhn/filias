# $Id: sql.py,v 1.1 2015/05/05 07:22:10 dhn Exp $
# -*- coding: utf-8 -*-

import sqlite3

# conn = sqlite3.connect(":memory:")
conn = sqlite3.connect("./ILIAS.sql")


# create SQL table
def create_db():
    state = False
    try:
        with conn:
            conn.execute(" \
                CREATE TABLE IF NOT EXISTS files ( \
                title TEXT NOT NULL, \
                obj_id INT, \
                parent_id INT, \
                last_update TEXT, \
                file_size INT, \
                types TEXT NOT NULL, \
                UNIQUE (title, obj_id)) \
            ")
            state = True
    except sqlite3.Error as error:
        print("An error occurred:", error.args[0])
        conn.close()
    return state


# Add thing into SQL
def insert_into_db(title, obj_id, parent_id, last_update, file_size, types):
    try:
        with conn:
            conn.execute(" \
                INSERT OR IGNORE INTO files (title, obj_id, parent_id, \
                                             last_update, file_size, types) \
                VALUES (?, ?, ?, ?, ?, ?)", (title, obj_id, parent_id,
                                             last_update, file_size, types))
    except sqlite3.Error as error:
        print("An error occurred:", error.args[0])
        conn.close()


# Get Course Name from SQL
def getCourseName():
    try:
        with conn:
            result = conn.execute("SELECT title FROM files \
                    WHERE types='crs' \
                    ORDER BY title").fetchall()
    except sqlite3.Error as error:
        print("An error occurred:", error.args[0])
        conn.close()
    return result


# Get Object Parent Title from SQL
def getParentTitle(obj_id):
    try:
        with conn:
            result = conn.execute("SELECT title FROM files \
                    WHERE obj_id = (SELECT parent_id FROM files \
                    WHERE obj_id = ?)", (obj_id,)).fetchone()
    except sqlite3.Error as error:
        print("An error occurred:", error.args[0])
        conn.close()
    return result


# Get All Information from SQL
def getAllInformation():
    try:
        with conn:
            result = conn.execute("SELECT * FROM files").fetchall()
    except sqlite3.Error as error:
        print("An error occurred:", error.args[0])
        conn.close()
    return result
