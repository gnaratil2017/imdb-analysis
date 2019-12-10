import mysql.connector

cnx = mysql.connector.connect(user='root', password='MySQL2019', database='imdb')

curA = cnx.cursor(buffered=True)

query = (
	)

# query = ("")