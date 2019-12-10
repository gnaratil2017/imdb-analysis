import mysql.connector

mydb = mysql.connector.connect(user='root', passwd='ThisClassFuckingSucks666!', database='imdb')
mycursor = mydb.cursor()

def search(primaryTitle, genre, primaryName, titleType):
    primaryName = "%" + primaryName + "%"
    args = (primaryName, )
    query = ("SELECT * FROM name_basics WHERE primaryName LIKE %s")
    mycursor.execute(query, args)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

search("", "", "Ingmar Bergman", "")