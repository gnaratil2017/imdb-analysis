# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from python_sql_driver import search
from display import createTableSearch

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
             dcc.Markdown("## Search for films by title, genre, actors, or type"),
             dcc.Markdown("###### Type information into the input boxes to search for films."),
             html.Div("Enter a Title:"),
             dcc.Input(
                placeholder='Title',
                type='text',
                value='',
                id="search-title"),
             # genre input
             html.Div("Enter a Genre:"),
             dcc.Input(
                placeholder='Genre',
                type='text',
                value='',
                id="search-genre"),
             # actor input
             html.Div("Enter an Actor/Actress:"),
             dcc.Input(
                placeholder='Actor',
                type='text',
                value='',
                id="search-actor"),
             # type input
             html.Div("Enter a Type of Movie (alternative, dvd, festival, tv, video):"),
             dcc.Input(
                placeholder='Type',
                type='text',
                value='',
                id="search-type"),
             dbc.Button("Search for movies", color='success', id='search-button')]),
                
             dbc.Col(
                html.Div(["Movie Data"], id="search-movie-data"))])])


# body for the rank functionality
rank_body = html.Div([
    dbc.Row([dbc.Col([
            dcc.Markdown("## Rank films by genre, type, actor, year, etc."),  
            dcc.Markdown("##### Choose a category/attribute to rank by. Click the rank button to submit the ranking"),
            
            # filter stuff
            dbc.Row([dbc.Col([dcc.Markdown("###### Filter By Type:"),
                            dbc.Select(id = 'type-filter',
                                        options=[
                                            {'label':'Movies', 'value':'movie'},
                                            {'label':'Shorts', 'value':'short'},
                                            {'label':'TV Series', 'value':'tvSeries'}],
                                        value="movie")]),
                     dbc.Col([dcc.Markdown("###### Choose minimum ratings for ranked films:"),
                              dbc.Input(id="min-ratings", value=10000, type='number', min=0, step=1)])]),
            html.Br(),
            dcc.Markdown("###### Rank by Genre:"),
            dbc.Row([dbc.Col(dbc.Select(id='genre-rank',
                                       options=[
                                            {'label': 'stand-in', 'value': 'null'}])),
                    dbc.Col(dbc.Button("Rank!", color='success', id='genre-rank-button'))]),
            html.Br(),
            dcc.Markdown("###### Rank by Type (note this overrides the type filter above):"),
            dbc.Row([dbc.Col(dbc.Select(id='type-rank',
                                        options=[
                                                {'label':'Movies', 'value':'movie'},
                                                {'label':'Shorts', 'value':'short'},
                                                {'label':'TV Series', 'value':'tvSeries'}])),
                    dbc.Col(dbc.Button("Rank!", color='success', id='type-rank-button'))]),
            html.Br(),
            dcc.Markdown("###### Rank by Time Period (will rank all movies within the range below):"),
            dbc.Row([dbc.Col(dcc.Markdown("###### Start Year:")),
                    dbc.Col(dcc.Markdown("###### End Year:")),
                    dbc.Col()]),
            dbc.Row([dbc.Col(dbc.Input(id="range-rank-start", placeholder='Start year...', type='text')),
                    dbc.Col(dbc.Input(id="range-rank-end", placeholder='End year...', type='text')),
                    dbc.Col(dbc.Button("Rank!", color='success', id='range-rank-button'))]),
            html.Br(),
            dcc.Markdown("###### Rank by Single Year:"),
            dbc.Row([dbc.Col(dbc.Input(id="year-rank", placeholder='Enter year...', type='text')),
                    dbc.Col(dbc.Button("Rank!", color='success', id='year-rank-button'))]),
            html.Br(),
            dcc.Markdown("###### Rank by Actor:"),
            dbc.Row([dbc.Col(dbc.Input(id="actor-rank", placeholder='Enter actor...', type='text')),
                    dbc.Col(dbc.Button("Rank!", color='success', id='actor-rank-button'))])]),

            # begin data entry side of page
            dbc.Col(
                html.Div("No Ranking Selected", id="rank-data"))])])
# 1892


# body for the reccomend functionality
recommend_body = html.Div([
    html.Div("Choose a movie and we will reccomend highly rated movies that are similar:"),
    dcc.Dropdown(
        # TODO: write a function to generate these options, values can be the ids
        options=[
            {'label': 'Iron Man 3', 'value': '102044'},
            {'label': 'Interstellar', 'value': '923402'},
            {'label': 'Inception', 'value': '0293432'}
        ],
        value='MTL'),])


app.layout = html.Div([navbar, body])


#callback for the search function
@app.callback(
    Output("search-movie-data", "children"),
    [Input("search-button", "n_clicks")],
    [State('search-title', "value"),
     State('search-genre', "value"),
     State('search-actor', "value"),
     State('search-type', "value")]
)
def search_for_movie(search_click, title_value, genre_value, actor_value, type_value):
    # data = search(title_value, genre_value, actor_value, type_value)
    if title_value == '' and genre_value == '' and actor_value == '' and type_value == '':
        return "No Movie Searched For"
    else:
        data = search(title_value, genre_value, actor_value, type_value)
        table = createTableSearch(data)
        return table

# callback for ranking
# @app.callback(
#     Output("search-movie-data", "children"),
#     [Input("search-title", "value")]
# )
# def search_for_movie(movie_string):
#     return movie_string

# callback for recommendations
# @app.callback(
#     Output("search-movie-data", "children"),
#     [Input("search-title", "value")]
# )
# def search_for_movie(movie_string):
#     return movie_string


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