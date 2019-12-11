import mysql.connector

mydb = mysql.connector.connect(user='root', password='ThisClassFuckingSucks666!', database='imdb')
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
