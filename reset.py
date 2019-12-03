import sqlite3   #enable control of an sqlite database

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

command = "DROP TABLE IF EXISTS users;" # delete table
c.execute(command)

command = "DROP TABLE IF EXISTS apiKeys;" # delete table
c.execute(command)

command = "CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, password TEXT, firstName TEXT, lastName TEXT, email TEXT, phoneNum TEXT, location TEXT, ip TEXT, address TEXT);" # create table
c.execute(command)    # run SQL statement

command = "CREATE TABLE IF NOT EXISTS apiKeys (id INTEGER, openWeather TEXT, fullContact TEXT, googleCivic TEXT, locationIQ TEXT, googleMaps TEXT);" # create table
c.execute(command)    # run SQL statement

db.commit()
db.close()
