import mysql.connector

def connectToDB():
	db = mysql.connector.connect(
		user="root",
		password="MySQL2019",
		database="imdb"
		)
	return db

db = connectToDB()
mycursor = db.cursor()

def getTitles(primaryTitle):
	args = (primaryTitle, )
	Q = "SELECT tconst, primaryTitle FROM title_basics_with_ratings WHERE primaryTitle LIKE CONCAT('%', %s, '%') ORDER BY numVotes DESC LIMIT 5"
	mycursor.execute(Q, args)
	data = mycursor.fetchall()
	return data

print(getTitles("Iron Man"))