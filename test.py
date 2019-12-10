import mysql.connector

db = mysql.connector.connect(
	host="localhost",
	user="root",
	password="tw1-olmani",
	database="movies"
	)

mycursor = db.cursor()

mycursor.execute("DESCRIBE name_basics")

for x in mycursor:
	print(x)
