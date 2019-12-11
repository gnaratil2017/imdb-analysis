# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from python_sql_driver import search
from display import *
from ranking_new import *
from recommendations import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# required because not all callback inputs and outputs are present upon loading
app.config.suppress_callback_exceptions = True

# this sets up the basic navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("See Code", href="https://github.com/gnaratil2017/imdb-analysis")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Search for Movies", id = "search", n_clicks_timestamp='0'),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("See Rankings", id = "rank", n_clicks_timestamp='0'),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Get Movie Recommendations", id = "recommend", n_clicks_timestamp='0'),
            ],
            id = "nav-dropdown"
        ),
    ],
    brand="Movie Central - Brought to you by Daniel, Greg, Tom, and Tom",
    brand_href="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    sticky="top",
)

# this is the placeholder for the body, the body changes depending on what function the user wants (search, rank, recommend)
body = html.Div(id="body-hold", className="mt-3")

# the body for the search functionality
# might want to put these all in rows so they are spaced out
search_body = html.Div([
    dbc.Row([dbc.Col([
                # title input
             dcc.Markdown("# Search!"),
             dcc.Markdown("#### Search for films by title, genre, person involved, or type"),
             dcc.Markdown("##### Type information into the input boxes to search for films."),
             html.Br(),
             dcc.Markdown("###### Enter a Title:"),
             dcc.Input(
                placeholder='Title...',
                type='text',
                value='',
                id="search-title"),
             # genre input
             html.Br(),
             html.Br(),
             dcc.Markdown("###### Enter a Genre:"),
             dcc.Input(
                placeholder='Genre...',
                type='text',
                value='',
                id="search-genre"),
             # actor input
             html.Br(),
             html.Br(),
             dcc.Markdown("###### Enter a person involved in making movies:"),
             dcc.Input(
                placeholder='Person...',
                type='text',
                value='',
                id="search-person"),
             # type input
             html.Br(),
             html.Br(),
             dcc.Markdown("###### Enter a Type of Movie (alternative, dvd, festival, tv, video):"),
             dcc.Input(
                placeholder='Type...',
                type='text',
                value='',
                id="search-type"),
             html.Br(),
             html.Br(),
             dbc.Row(dbc.Col(dbc.Button("Search for movies", color='success', id='search-button')))]),
                
             dbc.Col(
                html.Div(["Movie Data"], id="search-movie-data"))])])


# body for the rank functionality
rank_body = html.Div([
    dbc.Row([dbc.Col([
            dcc.Markdown("## Rank films by genre, type, actor, year"),  
            dcc.Markdown("##### Choose a category/attribute to rank by. Click the rank button to submit the ranking."),
            dcc.Markdown("##### If no results are appearing, try reducing the minimum number of rankings filter."),
            # filter stuff
            dbc.Row([dbc.Col([dcc.Markdown("###### Filter By Type:"),
                            dbc.Select(id = 'type-filter',
                                        options=[
                                            {'label':'Movies', 'value':'movie'},
                                            {'label':'Shorts', 'value':'short'},
                                            {'label':'TV Series', 'value':'tvSeries'}],
                                        value="movie")]),
                     dbc.Col([dcc.Markdown("###### Choose minimum ratings for ranked films:"),
                              dbc.Input(id="min-ratings", value=500000, type='number', min=0, step=1)])]),
            html.Br(),
            dcc.Markdown("###### Rank by Genre:"),
            dbc.Row([dbc.Col(dbc.Select(id='genre-rank',
                                       options=[
                                            {'label':'Action', 'value':'Action'},
                                            {'label':'Adventure', 'value':'Adventure'},
                                            {'label':'Animation', 'value':'Animation'},
                                            {'label':'Biography', 'value':'Biography'},
                                            {'label':'Comedy', 'value':'Comedy'},
                                            {'label':'Crime', 'value':'Crime'},
                                            {'label':'Documentary', 'value':'Documentary'},
                                            {'label':'Drama', 'value':'Drama'},
                                            {'label':'Family', 'value':'Family'},
                                            {'label':'Fantasy', 'value':'Fantasy'},
                                            {'label':'Film-Noir', 'value':'Film-Noir'},
                                            {'label':'Game-Show', 'value':'Game-Show'},
                                            {'label':'History', 'value':'History'},
                                            {'label':'Horror', 'value':'Horror'},
                                            {'label':'Music', 'value':'Music'},
                                            {'label':'Musical', 'value':'Musical'},
                                            {'label':'Mystery', 'value':'Mystery'},
                                            {'label':'News', 'value':'News'},
                                            {'label':'Reality-TV', 'value':'Reality-TV'},
                                            {'label':'Romance', 'value':'Romance'},
                                            {'label':'Sci-Fi', 'value':'Sci-Fi'},
                                            {'label':'Sport', 'value':'Sport'},
                                            {'label':'TalkShow', 'value':'TalkShow'},
                                            {'label':'Thriller', 'value':'Thriller'},
                                            {'label':'War', 'value':'War'},
                                            {'label':'Western', 'value':'Western'}])),
                    dbc.Col(dbc.Button("Rank!", color='success', id='genre-rank-button', n_clicks_timestamp=0))]),
            html.Br(),
            dcc.Markdown("###### Rank by Type (note this overrides the type filter above):"),
            dbc.Row([dbc.Col(dbc.Select(id='type-rank',
                                        options=[
                                                {'label':'Movies', 'value':'movie'},
                                                {'label':'Short', 'value':'short'},
                                                {'label':'TV Mini-Series', 'value':'tvMiniSeries'},
                                                {'label':'TV Series', 'value':'tvSeries'},
                                                {'label':'TV Short', 'value':'tvShort'},
                                                {'label':'TV Special', 'value':'tvSpecial'},
                                                {'label':'TV Movie', 'value':'tvMovie'},
                                                {'label':'Video', 'value':'video'},
                                                {'label':'Video Game', 'value':'videoGame'}])),
                    dbc.Col(dbc.Button("Rank!", color='success', id='type-rank-button', n_clicks_timestamp=0))]),
            html.Br(),
            dcc.Markdown("###### Rank by Time Period (will rank all movies within the range below):"),
            dbc.Row([dbc.Col(dcc.Markdown("###### Start Year:")),
                    dbc.Col(dcc.Markdown("###### End Year:")),
                    dbc.Col()]),
            dbc.Row([dbc.Col(dbc.Input(id="range-rank-start", placeholder='Start year...', type='text')),
                    dbc.Col(dbc.Input(id="range-rank-end", placeholder='End year...', type='text')),
                    dbc.Col(dbc.Button("Rank!", color='success', id='range-rank-button', n_clicks_timestamp=0))]),
            html.Br(),
            dcc.Markdown("###### Rank by Single Year:"),
            dbc.Row([dbc.Col(dbc.Input(id="year-rank", placeholder='Enter year...', type='text')),
                    dbc.Col(dbc.Button("Rank!", color='success', id='year-rank-button',n_clicks_timestamp=0))]),
            html.Br(),
            dcc.Markdown("###### Rank by Actor:"),
            dbc.Row([dbc.Col(dbc.Input(id="actor-rank", placeholder='Enter actor...', type='text')),
                    dbc.Col(dbc.Button("Rank!", color='success', id='actor-rank-button',n_clicks_timestamp=0))])]),

            # begin data side of page
            dbc.Col(
                html.Div("No Ranking Selected", id="rank-data"))])])


# body for the reccomend functionality
recommend_body = html.Div([
    dbc.Row([dbc.Col([
            dcc.Markdown("# Best Recommendations"),
            dcc.Markdown("##### Type a movie in the box below and click search."),
            dcc.Markdown("##### The five buttons below will then update with movie titles."),
            dcc.Markdown("##### To get recommendations, just click go next to the movie you want."),
            html.Br(),
            dcc.Markdown("###### Search for Movie:"),
            dbc.Row([dbc.Col(dbc.Input(id='rec-movie-entry', placeholder='Enter movie...', type='text')),
                    dbc.Col(dbc.Button("Search!", id='rec-movie-button', color='success', n_clicks_timestamp=0))]),
            html.Br(),
            dcc.Markdown("###### Select one of the movies below to get recommendations for:"),
            dbc.Row([dbc.Col(dcc.Markdown("Production 1", id='rec1-label'), width='auto'),
                    dbc.Col(dbc.Button("Go!", id='rec1-go', color='success', n_clicks_timestamp=0))]),
            html.Br(),
            dbc.Row([dbc.Col(dcc.Markdown("Production 2", id='rec2-label'), width='auto'),
                    dbc.Col(dbc.Button("Go!", id='rec2-go', color='success', n_clicks_timestamp=0))]),
            html.Br(),
            dbc.Row([dbc.Col(dcc.Markdown("Production 3", id='rec3-label'), width='auto'),
                    dbc.Col(dbc.Button("Go!", id='rec3-go', color='success', n_clicks_timestamp=0))]),
            html.Br(),
            dbc.Row([dbc.Col(dcc.Markdown("Production 4", id='rec4-label'), width='auto'),
                    dbc.Col(dbc.Button("Go!", id='rec4-go', color='success', n_clicks_timestamp=0))]),
            html.Br(),
            dbc.Row([dbc.Col(dcc.Markdown("Production 5", id='rec5-label'), width='auto'),
                    dbc.Col(dbc.Button("Go!", id='rec5-go', color='success', n_clicks_timestamp=0))]),
            html.Div("tt1375666", id='rec1-data', style={'display' : 'none'}),
            html.Div("tt0468569", id='rec2-data', style={'display' : 'none'}),
            html.Div("tt0083658", id='rec3-data', style={'display' : 'none'}),
            html.Div("tt3315342", id='rec4-data', style={'display' : 'none'}),
            html.Div("tt0090605", id='rec5-data', style={'display' : 'none'}),
            ]),
            dbc.Col(
                html.Div("No Recommendations Yet", id="recommend-data"))])])


app.layout = html.Div([navbar, body])


#callback for the search function
@app.callback(
    Output("search-movie-data", "children"),
    [Input("search-button", "n_clicks")],
    [State('search-title', "value"),
     State('search-genre', "value"),
     State('search-person', "value"),
     State('search-type', "value")]
)
def search_for_movie(search_click, title_value, genre_value, person_value, type_value):
    # data = search(title_value, genre_value, person_value, type_value)
    if title_value == '' and genre_value == '' and person_value == '' and type_value == '':
        return "No Movie Searched For"
    else:
        data = search(title_value, genre_value, person_value, type_value)
        table = createTableSearch(data)
        return table


#callback for ranking function
@app.callback(
    Output("rank-data", "children"),
    [Input("genre-rank-button", "n_clicks_timestamp"),
     Input("type-rank-button", "n_clicks_timestamp"),
     Input("range-rank-button", "n_clicks_timestamp"),
     Input("year-rank-button", "n_clicks_timestamp"),
     Input("actor-rank-button", "n_clicks_timestamp")],
    [State('type-filter', 'value'),
     State('min-ratings', "value"),
     State('genre-rank', "value"),
     State('type-rank', "value"),
     State('range-rank-start', "value"),
     State('range-rank-end', "value"),
     State('year-rank', "value"),
     State('actor-rank', 'value')]
)
def search_for_movie(genre_click, type_click, range_click, year_click, actor_click, type_filter, ratings_filter, genre_data, type_data, range_start, range_end, year_data, actor_data):
    if genre_click == 0 and type_click == 0 and range_click == 0 and year_click == 0 and actor_click == 0:
        return "Submit a ranking on the left!"
    max_time = max(genre_click, type_click, range_click, year_click, actor_click)

    if max_time == genre_click:
        data = rankedByGenre(type_filter, genre_data, ratings_filter, 25)
        table = createTableRank(data)
        return table

    if max_time == type_click:
        data = rankedByType(type_data, ratings_filter, 25)
        table = createTableRank(data) 
        return table

    if max_time == range_click:
        data = rankedByTimePeriod(type_filter, range_start, range_end, ratings_filter, 25)
        table = createTableRank(data)
        return table

    if max_time == year_click:
        data = rankedByYear(type_filter, year_data, ratings_filter, 25)
        table = createTableRank(data)
        return table

    if max_time == actor_click:
        data = rankedByActor(type_filter, actor_data, ratings_filter, 25)
        table = createTableRank(data)
        return table

    return max_time


#callback for generating the options for recommendations
@app.callback(
    [Output("rec1-data", "children"),
     Output("rec2-data", "children"),
     Output("rec3-data", "children"),
     Output("rec4-data", "children"),
     Output("rec5-data", "children"),
     Output("rec1-label", "children"),
     Output("rec2-label", "children"),
     Output("rec3-label", "children"),
     Output("rec4-label", "children"),
     Output("rec5-label", "children")],
     [Input("rec-movie-button", "n_clicks")],
     [State("rec-movie-entry", "value")])
def find_movie_options(n_click, search_title):
    if n_click == 0:
        return "tt1375666", "tt0468569", "tt0083658", "tt3315342", "tt0090605", "Production 1", "Production 2", "Production 3", "Production 4", "Production 5"
    data = getTitles(search_title)
    if len(data) == 0:
        return "tt1375666", "tt0468569", "tt0083658", "tt3315342", "tt0090605", "Production 1", "Production 2", "Production 3", "Production 4", "Production 5"
    if len(data) == 1:
        return data[0][0], "tt0468569", "tt0083658", "tt3315342", "tt0090605", data[0][1], "Production 2", "Production 3", "Production 4", "Production 5"
    if len(data) == 2:
        return data[0][0], data[1][0], "tt0083658", "tt3315342", "tt0090605", data[0][1], data[1][1], "Production 3", "Production 4", "Production 5"
    if len(data) == 3:
        return data[0][0], data[1][0], data[2][0], "tt3315342", "tt0090605", data[0][1], data[1][1], data[2][1], "Production 4", "Production 5"
    if len(data) == 4:
        return data[0][0], data[1][0], data[2][0], data[3][0], "tt0090605", data[0][1], data[1][1], data[2][1], data[3][1], "Production 5"
    if len(data) == 5:
        return data[0][0], data[1][0], data[2][0], data[3][0], data[4][0], data[0][1], data[1][1], data[2][1], data[3][1], data[4][1]
    return none

#callback for recommendations generation
@app.callback(
    Output("recommend-data", "children"),
    [Input("rec1-go", "n_clicks_timestamp"),
     Input("rec2-go", "n_clicks_timestamp"),
     Input("rec3-go", "n_clicks_timestamp"),
     Input("rec4-go", "n_clicks_timestamp"),
     Input("rec5-go", "n_clicks_timestamp")],
    [State('rec1-data', 'children'),
     State('rec2-data', "children"),
     State('rec3-data', "children"),
     State('rec4-data', "children"),
     State('rec5-data', "children")]
)
def recommend_movie(rec1_click, rec2_click, rec3_click, rec4_click, rec5_click, rec1_data, rec2_data, rec3_data, rec4_data, rec5_data):
    if rec1_click == 0 and rec2_click == 0 and rec3_click == 0 and rec4_click == 0 and rec5_click == 0:
        return "Submit a recommendation on the left!"
    max_time = max(rec1_click, rec2_click, rec3_click, rec4_click, rec5_click)

    if max_time == rec1_click:
        # data = rankedByGenre(type_filter, genre_data, ratings_filter, 25)
        # table = createTableRank(data)
        return rec1_data

    if max_time == rec2_click:
        # data = rankedByType(type_data, ratings_filter, 25)
        # table = createTableRank(data) 
        return rec2_data

    if max_time == rec3_click:
        # data = rankedByTimePeriod(type_filter, range_start, range_end, ratings_filter, 25)
        # table = createTableRank(data)
        return rec3_data

    if max_time == rec4_click:
        # data = rankedByYear(type_filter, year_data, ratings_filter, 25)
        # table = createTableRank(data)
        return rec4_data

    if max_time == rec5_click:
        # data = rankedByActor(type_filter, actor_data, ratings_filter, 25)
        # table = createTableRank(data)
        return rec5_data

    return max_time



# callback to toggle the different parts of the app
@app.callback(
    Output("body-hold", "children"),
    [Input("search", "n_clicks_timestamp"),
     Input("rank", "n_clicks_timestamp"),
     Input("recommend", "n_clicks_timestamp")],
)
def update_application_view(search_click, rank_click, recommend_click):
    if int(search_click) > int(rank_click) and int(search_click) > int(recommend_click):
        return search_body
    elif int(rank_click) > int(search_click) and int(rank_click) > int(recommend_click):
        return rank_body
    elif int(recommend_click) > int(rank_click) and int(recommend_click) > int(search_click):
        return recommend_body
    else:
        return search_body


if __name__ == '__main__':
    app.run_server(debug=True)