import mysql.connector

def connectToDB():
	db = mysql.connector.connect(
		user="root",
		password="ThisClassFuckingSucks666!",
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

def get_tconst_data(tconst):
	data = []
	args = (tconst, )
	query = ("SELECT titleType, primaryTitle, isAdult, startYear, genres, directors, writers FROM title_basics_with_ratings_and_crew WHERE tconst = %s")
	mycursor.execute(query, args)
	data = mycursor.fetchall()
	return data

def getSimilarTitles(tconst):
	result = []
	tconst_data = get_tconst_data(tconst)[0]
	titleType = tconst_data[0]
	primaryTitle = tconst_data[1]
	isAdult = tconst_data[2]
	startYear = tconst_data[3]
	if (tconst_data[4]):
		genres = tconst_data[4].split(",")
	else:
		genres = []
	if (tconst_data[5]):
		directors = tconst_data[5].split(",")
	else:
		directors = []
	if (tconst_data[6]):
		writers = tconst_data[6].split(",")
	else:
		writers = []
	minYear = str(int(startYear) - 10)
	maxYear = str(int(startYear) + 10)
	
	args = [titleType, isAdult, minYear, maxYear] + genres + directors + writers
	
	cases = ["CASE WHEN titleType = %s THEN 1 ELSE 0 END",
				"CASE WHEN isAdult = %s THEN 1 ELSE 0 END",
				"CASE WHEN startYear BETWEEN %s AND %s THEN 1 ELSE 0 END",
				" + ".join(["CASE WHEN genres LIKE CONCAT('%', %s, '%') THEN 1 ELSE 0 END" for genre in genres]),
				" + ".join(["CASE WHEN directors LIKE CONCAT('%', %s, '%') THEN 1 ELSE 0 END" for director in directors]),
				" + ".join(["CASE WHEN writers LIKE CONCAT('%', %s, '%') THEN 1 ELSE 0 END" for writer in writers])]

	while "" in cases:
		cases.remove("")

	query = ("SELECT tconst, primaryTitle, startYear, genres, averageRating, numVotes, " + " + ".join(cases) + \
		" AS score FROM title_basics_with_ratings_and_crew ORDER BY score DESC LIMIT 10")
		
	mycursor.execute(query, args)
	result = mycursor.fetchall()
	return result
