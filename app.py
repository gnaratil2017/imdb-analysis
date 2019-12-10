# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# from python_sql_driver import search

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
# thinking about potentially making these into dropdowns instead of inputs
search_body = html.Div([
    dbc.Row([dbc.Col(
                # title input
                [dcc.Markdown("## Search for movies by title, genre, actors, or type!"),
                 dcc.Markdown("###### Type information into one of the input boxes below and click the corresponding button to search for movies."),
                 html.Div("Enter a Title:"),
                 dcc.Input(
                    placeholder='Title',
                    type='text',
                    value='',
                    id="search-title"),
                 html.Button("Search for movies based on title", id='title-button', n_clicks_timestamp=0),
                 # genre input
                 html.Div("Enter a Genre:"),
                 dcc.Input(
                    placeholder='Genre',
                    type='text',
                    value='',
                    id="search-genre"),
                 html.Button("Search for movies of the same genre", id='genre-button', n_clicks_timestamp=0),
                 # actor input
                 html.Div("Enter an Actor/Actress:"),
                 dcc.Input(
                    placeholder='Actor',
                    type='text',
                    value='',
                    id="search-actor"),
                 html.Button("Search for movies by actor/actress", id='actor-button', n_clicks_timestamp=0),
                 # type input
                 html.Div("Enter a Type of Movie (alternative, dvd, festival, tv, video):"),
                 dcc.Input(
                    placeholder='Type',
                    type='text',
                    value='',
                    id="search-type"),
                 html.Button("Search for movies of the same type", id='type-button', n_clicks_timestamp=0)]),
                
             dbc.Col(
                html.Div(["Movie Data"], id="search-movie-data"))])])

# body for the rank functionality
rank_body = html.Div([
    html.Div("Choose a category/attribute to rank by:"),
    # TODO: write a function to generate these options
    dcc.Dropdown(
        options=[
            {'label': 'Genre - Comedy', 'value': 'g_comedy'},
            {'label': 'Year - 2016', 'value': 'y_2016'},
            {'label': 'Actor - Emily Blunt', 'value': 'a_emily_blunt'}
        ],
        value='MTL'),
    html.Div("Top Movies:"),
    html.Div(id="rank-movie-data")])

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
# search() takes 5 arguments, the four values of the input boxes and what button was clicked
# 1 for title, 2 for genre, 3 for actor, 4 for type
@app.callback(
    Output("search-movie-data", "children"),
    [Input("title-button", "n_clicks_timestamp"),
     Input("genre-button", "n_clicks_timestamp"),
     Input("actor-button", "n_clicks_timestamp"),
     Input("type-button", "n_clicks_timestamp")],
    [State('search-title', "value"),
     State('search-genre', "value"),
     State('search-actor', "value"),
     State('search-type', "value")]
)
def search_for_movie(title_click, genre_click, actor_click, type_click, title_value, genre_value, actor_value, type_value):
    time_max = max(int(title_click), int(genre_click), int(actor_click), int(type_click))
    if time_max == int(title_click):
        # data = search(title_value, genre_value, actor_value, type_value, 1)
        data = title_value
    if time_max == int(genre_click):
        # data = search(title_value, genre_value, actor_value, type_value, 2)
        data = genre_value
    if time_max == int(actor_click):
        # data = search(title_value, genre_value, actor_value, type_value, 3)
        data = actor_value
    if time_max == int(type_click):
        # data = search(title_value, genre_value, actor_value, type_value, 4)
        data = type_value
    return data

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