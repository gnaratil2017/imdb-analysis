# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from python_sql_driver import search

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
                [html.Div("Enter a Title:"),
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
                    placeholder='Language',
                    type='text',
                    value='',
                    id="search-language"),
                 html.Button("Search for Movies", id='search-button')]),
                # could add a region or language search as well
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

#callback for the search function, will incorporate all of the different values
@app.callback(
    Output("search-movie-data", "children"),
    [Input("search-title", "value")]
)
def search_for_movie(movie_string):
    return movie_string

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