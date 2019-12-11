import mysql.connector

mydb = mysql.connector.connect(user='root', password='MySQL2019', database='imdb')
mycursor = mydb.cursor()

def getGenreAvgRatings():
    genres = ['%Action%', '%Comedy%', '%Documentary%', '%Drama%', '%Horror%', '%Romance%']
    data = []
    for genre in genres:
        args = (genre, )
        query = "SELECT AVG(averageRating) FROM title_basics_with_ratings WHERE titleType = 'movie' AND genres LIKE %s"
        mycursor.execute(query, args)
        data.append(float(mycursor.fetchall()[0][0]))
    return data

def getGenreAvgRuntimes():
    genres = ['%Action%', '%Comedy%', '%Documentary%', '%Drama%', '%Horror%', '%Romance%']
    data = []
    for genre in genres:
        args = (genre, )
        query = "SELECT AVG(runtimeMinutes) FROM title_basics WHERE titleType = 'movie' AND genres LIKE %s"
        mycursor.execute(query, args)
        data.append(float(mycursor.fetchall()[0][0]))
    return data

def getTypeAvgRuntimes():
    titleTypes = ['movie', 'short', 'tvEpisode', 'tvMovie']
    data = []
    for titleType in titleTypes:
        args = (titleType, )
        query = "SELECT AVG(runtimeMinutes) FROM title_basics WHERE titleType = %s"
        mycursor.execute(query, args)
        data.append(float(mycursor.fetchall()[0][0]))
    return data

def connectToDB():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL2019",
        database="imdb"
        )
    return db


genres = ["Action", "Comedy", "Documentary", "Drama", "Horror", "Romance"]
types = ["movie", "tvEpisode", "short", "tvMovie"]

def extractDatapoints(results):
    x = []
    y = []
    for result in results:
        x.append(result[0])
        y.append(result[1])

    return x, y

# returns years, numMovies
def numMoviesYear(year1, year2):
    t1 = (year1, year2)
    db = connectToDB()
    mycursor = db.cursor()

    Q = "SELECT startYear, count(tconst) FROM title_basics_with_ratings WHERE startYear >= %s AND startYear <= %s GROUP BY startYear ORDER BY startYear;"

    mycursor.execute(Q, t1)

    results = mycursor.fetchall()
    return extractDatapoints(results)

# returns 3
def mostProducedTypesPerYear(year1, year2):
    db = connectToDB()
    mycursor = db.cursor()

    x_points = []
    y_points = []
    t1 = (year1, year2)
    for titleType in types:
        t2 = titleType,
        Q = "SELECT startYear, count(titleType) FROM title_basics_with_ratings WHERE startYear >= %s AND startYear <= %s AND titleType = %s GROUP BY startYear ORDER BY startYear;"
        mycursor.execute(Q, t1+t2)

        results = mycursor.fetchall()
        x_pointsType, y_pointsType = extractDatapoints(results)
        x_points.append(x_pointsType)
        y_points.append(y_pointsType)

    return types, x_points, y_points

# returns 2
def mostProducedGenreAllTime():
    db = connectToDB()
    mycursor = db.cursor()

    datapoints = []
    for genre in genres:
        t1 = (genre,)
        mycursor.execute("SELECT COUNT(tconst) FROM title_basics_with_ratings WHERE genres LIKE CONCAT('%', %s, '%');", t1)
        results = mycursor.fetchall()
        datapoints.append(results[0][0])

    return genres, datapoints

# print(mostProducedTypesPerYear("1950", "2010"))
