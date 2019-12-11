import mysql.connector

mydb = mysql.connector.connect(user='root', password='MySQL2019', database='imdb')
mycursor = mydb.cursor()

def get_tconst_data(tconsts, primaryTitle, genre, titleType):
    data = []
    base_query = ("SELECT tconst, titleType, primaryTitle, startYear, runtimeMinutes, genres, averageRating, numVotes FROM title_basics_with_ratings WHERE tconst = %s")
    add_to_query = ""
    add_to_args = ()
    primaryTitleWhere = "primaryTitle LIKE %s"
    genreWhere = "genres LIKE %s"
    titleTypeWhere = "titleType LIKE %s"

    if primaryTitle != "%%" and genre != "%%" and titleType != "%%":
        add_to_args = (titleType, primaryTitle, genre)
        add_to_query = " AND " + titleTypeWhere + " AND " + primaryTitleWhere + " AND " + genreWhere
    
    elif primaryTitle != "%%" and genre != "%%":
        add_to_args = (primaryTitle, genre)
        add_to_query = " AND " + primaryTitleWhere + " AND " + genreWhere

    elif titleType != "%%" and genre != "%%":
        add_to_args = (titleType, genre)
        add_to_query = " AND " + titleType + " AND " + genreWhere
    
    elif primaryTitle != "%%" and titleType != "%%":
        add_to_args = (titleType, primaryTitle)
        add_to_query = " AND " + titleTypeWhere + " AND " + primaryTitleWhere
    
    elif titleType != "%%":
        add_to_args = (titleType, )
        add_to_query = " AND " + titleTypeWhere
    
    elif primaryTitle != "%%":
        add_to_args = (primaryTitle, )
        add_to_query = " AND " + primaryTitleWhere
    
    elif genre != "%%":
        add_to_args = (genre, )
        add_to_query = " AND " + genreWhere

    for tconst in tconsts:
        args = (tconst, ) + add_to_args
        query = (base_query + add_to_query)
        mycursor.execute(query, args)
        myresult = mycursor.fetchall()
        data.extend(myresult)
    return data

def search(primaryTitle, genre, primaryName, titleType):
    data = []
    primaryTitle = "%" + primaryTitle + "%"
    genre = "%" + genre + "%"
    primaryName = "%" + primaryName + "%"
    titleType = "%" + titleType + "%"
    primaryTitleWhere = "primaryTitle LIKE %s"
    genreWhere = "genres LIKE %s"
    primaryNameWhere = "primaryName LIKE %s"
    titleTypeWhere = "titleType LIKE %s"

    if primaryName != "%%":
        args = (primaryName, )
        query = ("SELECT knownForTitles FROM name_basics WHERE " + primaryNameWhere)
        mycursor.execute(query, args)
        myresult = mycursor.fetchall()
        for person in myresult:
            if person[0]:
                tconsts_str = person[0]
                tconsts_arr = tconsts_str.split(",")
                data.extend(get_tconst_data(tconsts_arr, primaryTitle, genre, titleType))

    elif primaryTitle != "%%" and genre != "%%" and titleType != "%%":
        args = (titleType, primaryTitle, genre)
        query = ("SELECT tconst, titleType, primaryTitle, startYear, runtimeMinutes, genres, averageRating, numVotes FROM title_basics_with_ratings WHERE " + titleTypeWhere + " AND " + primaryTitleWhere + " AND " + genreWhere)
        mycursor.execute(query, args)
        data = mycursor.fetchall()

    elif primaryTitle != "%%" and genre != "%%":
        args = (primaryTitle, genre)
        query = ("SELECT tconst, titleType, primaryTitle, startYear, runtimeMinutes, genres, averageRating, numVotes FROM title_basics_with_ratings WHERE " + primaryTitleWhere + " AND " + genreWhere)
        mycursor.execute(query, args)
        data = mycursor.fetchall()

    elif primaryTitle != "%%" and titleType != "%%":
        args = (titleType, primaryTitle)
        query = ("SELECT tconst, titleType, primaryTitle, startYear, runtimeMinutes, genres, averageRating, numVotes FROM title_basics_with_ratings WHERE " + titleTypeWhere + " AND " + primaryTitleWhere)
        mycursor.execute(query, args)
        data = mycursor.fetchall()

    elif genre != "%%" and titleType != "%%":
        args = (titleType, genre)
        query = ("SELECT tconst, titleType, primaryTitle, startYear, runtimeMinutes, genres, averageRating, numVotes FROM title_basics_with_ratings WHERE " + titleTypeWhere + " AND " + genreWhere)
        mycursor.execute(query, args)
        data = mycursor.fetchall()

    elif primaryTitle != "%%":
        args = (primaryTitle, )
        query = ("SELECT tconst, titleType, primaryTitle, startYear, runtimeMinutes, genres, averageRating, numVotes FROM title_basics_with_ratings WHERE " + primaryTitleWhere)
        mycursor.execute(query, args)
        data = mycursor.fetchall()
    
    elif genre != "%%":
        args = (genre, )
        query = ("SELECT tconst, titleType, primaryTitle, startYear, runtimeMinutes, genres, averageRating, numVotes FROM title_basics_with_ratings WHERE " + genreWhere)
        mycursor.execute(query, args)
        data = mycursor.fetchall()
        
    elif titleType != "%%":
        args = (titleType, )
        query = ("SELECT tconst, titleType, primaryTitle, startYear, runtimeMinutes, genres, averageRating, numVotes FROM title_basics_with_ratings WHERE " + titleTypeWhere)
        mycursor.execute(query, args)
        data = mycursor.fetchall()

    return data


