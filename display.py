import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from python_sql_driver import search

def createTableSearch(data):
	table_header = [html.Thead(html.Tr([html.Th("Movie Name"), html.Th("Genres"), html.Th("Rating"), html.Th("Runtime"), html.Th("Release Year")]))]
	
	rows = []

	for i in range(len(data)):
		print(data[i][6])
		row = html.Tr([html.Td(data[i][2]), html.Td(data[i][5]), html.Td(data[i][6]), html.Td(data[i][4]), html.Td(data[i][3])])
		rows.append(row)

	table_body = [html.Tbody(rows)]

	table = dbc.Table(table_header + table_body, bordered=True, striped = True, hover=True, dark=True)

	return table

# data_input = search("Iron Man", "", "", "movie")

# print(createTableSearch(data_input))

# print(search("Iron Man", "", "", "movie")[0])