import dash_core_components as dcc
import dash_html_components as html
from dashpackage.layouts import *
from dashpackage.queries import *
from dashpackage import app


app.layout = html.Div(children=[
    html.H1("Check it out! This app has Flask AND Dash!"),
    html.P("Adding some cool graph here soon:"),
    # dcc.Graph(
    #     id = "inudstry_job_data",
    #     figure = {
    #          'data' :industries_and_job_listings_donut_chart(),
    #          'layout' : donut_layout
    #     }
    # )
])
