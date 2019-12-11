import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from python_sql_driver import search
from stats import *
import plotly.graph_objects as go


def createTableSearch(data):
	table_header = [html.Thead(html.Tr([html.Th("Movie Name"), html.Th("Genres"), html.Th("Rating"), html.Th("Runtime"), html.Th("Release Year")]))]
	
	rows = []

	for i in range(len(data)):
		row = html.Tr([html.A(href = 'https://www.imdb.com/title/' + data[i][0] + '/', children = html.Td(data[i][2]), target='_blank'), html.Td(data[i][5]), html.Td(data[i][6]), html.Td(data[i][4]), html.Td(data[i][3])])
		rows.append(row)

	table_body = [html.Tbody(rows)]

	table = dbc.Table(table_header + table_body, bordered=True, striped = True, hover=True)

	return table

def createTableRank(data):
	table_header = [html.Thead(html.Tr([html.Th("Movie Name"), html.Th("Rating"), html.Th("Number of Ratings"), html.Th("Release Year")]))]
	
	rows = []

	for i in range(len(data)):
		row = html.Tr([html.A(href = 'https://www.imdb.com/title/' + data[i][0] + '/', children = html.Td(data[i][1]), target='_blank'), html.Td(data[i][3]), html.Td(data[i][4]), html.Td(data[i][2])])
		rows.append(row)

	table_body = [html.Tbody(rows)]

	table = dbc.Table(table_header + table_body, bordered=True, striped = True, hover=True)

	return table

def createTableRecommendation(data):
	table_header = [html.Thead(html.Tr([html.Th("Movie Name"), html.Th("Genre"), html.Th("Rating"), html.Th("Number of Ratings"), html.Th("Release Year")]))]
	
	rows = []

	for i in range(len(data)):
		row = html.Tr([html.A(href = 'https://www.imdb.com/title/' + data[i][0] + '/', children = html.Td(data[i][1]), target='_blank'), html.Td(data[i][3]), html.Td(data[i][4]), html.Td(data[i][5]), html.Td(data[i][2])])
		rows.append(row)

	table_body = [html.Tbody(rows)]

	table = dbc.Table(table_header + table_body, bordered=True, striped = True, hover=True)

	return table


def createGraphAvgRatings():
	y_data = getGenreAvgRatings()
	x_data = ['Action', 'Comedy', 'Documentary', 'Drama', 'Horror', 'Romance']
	data = [go.Bar(x=x_data, y=y_data, marker_color='#00bc8c', opacity=.6)]
	return go.Figure(data=data, layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_text = 'Average Rating by Genre',
            xaxis_title='Genre',
            yaxis_title='Rating',
            font=dict(color='#fff')))

def createGraphAvgRuntimes():
	y_data = getGenreAvgRuntimes()
	x_data = ['Action', 'Comedy', 'Documentary', 'Drama', 'Horror', 'Romance']
	data = [go.Bar(x=x_data, y=y_data, marker_color='#3498DB', opacity=.6)]
	return go.Figure(data=data, layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_text = 'Average Runtime by Genre',
            xaxis_title='Genre',
            yaxis_title='Runtime',
            font=dict(color='#fff')))

def createGraphAvgRuntimesType():
	y_data = getTypeAvgRuntimes()
	x_data = ['Movie', 'Short', 'TV Episodes', 'TV Movie']
	data = [go.Bar(x=x_data, y=y_data, marker_color='#F39C12', opacity=.6)]
	return go.Figure(data=data, layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_text = 'Average Runtime by Production',
            xaxis_title='Type of Production',
            yaxis_title='Runtime',
            font=dict(color='#fff')))

def createGraphGenreAllTime():
	x_data, y_data = mostProducedGenreAllTime()
	data = [go.Bar(x=x_data, y=y_data, marker_color='#E74C3C', opacity=.6)]
	return go.Figure(data=data, layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_text = 'Total Productions by Genre since 1900',
            xaxis_title='Type of Production',
            yaxis_title='Number of Productions',
            font=dict(color='#fff')))

def createGraphYearlyMovies():
	x_data, y_data = numMoviesYear(1950, 2010)
	data = [go.Scatter(x=x_data, y=y_data, mode = 'lines', marker_color='#e83e8c', opacity=.6, line=dict(width=3))]
	return go.Figure(data=data, layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_text = 'Movies per Year',
            xaxis_title='Year',
            yaxis_title='Number of Movies',
            font=dict(color='#fff')))

def createGraphTypeYearly():
	types, x_data, y_data = mostProducedTypesPerYear(1950, 2010)
	graph_data = []
	for i in range(len(types)):
		graph_data.append(go.Scatter(y=y_data[i], x=x_data[i], mode='lines', name=types[i], opacity=.6, line=dict(width=3)))
	return go.Figure(data=graph_data, layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_text = 'Productions per Year Broken Down By Type',
            xaxis_title='Year',
            yaxis_title='Number of Movies',
            font=dict(color='#fff')))


# data_input = search("Iron Man", "", "", "movie")

# print(createTableSearch(data_input))

# print(search("Iron Man", "", "", "movie")[0])

# tconst, primaryTitle, startYear, averageRating, numVotes