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

def sortByRating(item):
	return item[2]

def get_tconst_data(tconsts, titleType, numVotes):
	data = []
	query = "SELECT tconst, primaryTitle, startYear, averageRating, numVotes FROM title_basics_with_ratings WHERE tconst = %s AND titleType = %s AND numVotes >= %s"
	for tconst in tconsts:
		args = (tconst, titleType, numVotes)
		mycursor.execute(query, args)
		myresult = mycursor.fetchall()
		data.extend(myresult)

	return data

def rankedByActor(titleType, primaryName, numVotes, nElements):
	data = []

	primaryName = "%" + primaryName + "%"
	primaryNameWhere = "primaryName LIKE %s"

	if primaryName != "%%":
		args = (primaryName, )
		query = ("SELECT knownForTitles FROM name_basics WHERE " + primaryNameWhere)
		mycursor.execute(query, args)
		myresult = mycursor.fetchall()
		for person in myresult:
			if person[0]:
				tconsts_str = person[0]
				tconsts_arr = tconsts_str.split(",")
				data.extend(get_tconst_data(tconsts_arr, titleType, numVotes))
	
	sortedData = sorted(data, key=sortByRating, reverse=True)
	return sortedData[:nElements]

def rankedByType(filmtype, numVotes, nElements):
	t1 = (filmtype, numVotes, nElements)

	Q = "SELECT tconst, primaryTitle, startYear, averageRating, numVotes FROM title_basics_with_ratings WHERE titleType = %s AND numVotes >= %s ORDER BY averageRating DESC LIMIT %s"
	mycursor.execute(Q, t1)

	return mycursor.fetchall()

def rankedByTimePeriod(titleType, year1, year2, numVotes, nElements):
	t1 = (titleType, year1, year2, numVotes, nElements)

	Q = "SELECT tconst, primaryTitle, startYear, averageRating, numVotes FROM title_basics_with_ratings WHERE titleType = %s AND startYear >= %s AND startYear <= %s AND numVotes >= %s ORDER BY averageRating DESC LIMIT %s"
	mycursor.execute(Q, t1)

	return mycursor.fetchall()

def rankedByYear(titleType, year, numVotes, nElements):
	return rankedByTimePeriod(titleType, year, year, numVotes, nElements)

def rankedByGenre(titleType, genre, numVotes, nElements):
	t = (titleType, genre, numVotes, nElements)

	Q = "SELECT tconst, primaryTitle, startYear, averageRating, numVotes FROM title_basics_with_ratings WHERE titleType = %s AND genres LIKE CONCAT('%', %s, '%') AND numVotes >= %s ORDER BY averageRating DESC LIMIT %s"
	mycursor.execute(Q, t)
	
	return mycursor.fetchall()

# print(rankedByGenre("tvSeries","Game-Show", 0, 10))
# print(rankedByActor("movie","Tom Hanks", 0, 25))
# print(rankedByType("tvSeries", 10000, 25))