import mysql.connector

db = mysql.connector.connect(
	host="localhost",
	user="root",
	password="yourpassword",
	database="DBname"
	)

mycursor = db.cursor()

mycursor.execute("INSERT INTO table (attr1, attr2) VALUES (%s, %s)", (var1, var2))
db.commit()

mycursor.execute("SELECT * FROM table")

mycursor.execute("SELECT id, name FROM table WHERE gender = 'F' ORDER BY id DESC")

mycursor.execute("DESCRIBE name_basics")

for x in mycursor:
	print(x)
