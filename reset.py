import sqlite3   #enable control of an sqlite database

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

command = "DROP TABLE IF EXISTS users;" # delete table
c.execute(command)

command = "DROP TABLE IF EXISTS info;" # delete table
c.execute(command)

command = "CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, password TEXT);" # create table
c.execute(command)    # run SQL statement

command = "CREATE TABLE IF NOT EXISTS info (id INTEGER, firstName TEXT, lastName TEXT, email TEXT, phone TEXT, location TEXT);" # create table
c.execute(command)

db.commit()
db.close()
