import dash_core_components as dcc
import dash_html_components as html
from dashpackage.layouts import donut_layout
from dashpackage.queries import *
from dashpackage import app

data1 = industries_and_job_listings_donut_chart()
data2 = interactive_map_data()
app.layout = html.Div(children=[
    html.H1("Check it out! This app has Flask AND Dash!"),
    html.P("Adding some cool graph here soon:"),
    dcc.Graph(
        id = "inudstry_job_data1",
        figure = {
             'data' : data1,
             'layout' : donut_layout

            }),
    dcc.Graph(
        id = "inudstry_job_data2",
        figure = {
             'data' : data2[0],
             'layout' : data2[1]

            })
])


print('******Done with Dashboard******')
