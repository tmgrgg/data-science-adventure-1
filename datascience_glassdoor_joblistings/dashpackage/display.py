import dash_core_components as dcc
import dash_html_components as html
from dashpackage.layouts import donut_layout
from dashpackage.queries import interactive_map_data
from dashpackage import app


#this doens't need to be a callback yet as it won't be called on input
def geomap():
    map_data = interactive_map_data()
   # map_data[1]['margin'] = dict(l=10, r=10, t=0, b=0),
    print('LAYOUT', map_data[1])
    return {'data' : map_data[0], 'layout' : map_data[1]}


#layout = [
#    html.Div([
#            
#            html.Div([
#    
#            dcc.Graph(
#        id="map",
#        #style={"height": "90%", "width": "98%"},
#        #config=dict(displayModeBar=False),
#        style={"height": "90%", "width": "98%"},
#        config=dict(displayModeBar=False),
#        figure=geomap()
#        ),
#    dcc.Graph(
#        style={"height": "90%", "width": "98%"},
#        config=dict(displayModeBar=False),
#        )
#    ])
#    style={"marginTop": "5"},
#)
#    ]
    
layout = [
        
# charts row div
    html.Div(
        [
            html.Div(
                [
                    html.P("Leads count per state" ),
                    dcc.Graph(
                        id="map",
                       # style={"height": "90%", "width": "98%"},
                        figure=geomap(),
                        config=dict(displayModeBar=False),
                        style={'width':'100%', 'height':'100%'}
                    ),
                ],
                style={'width':'50%', 'display': 'inline-block'}
            ),

            
             html.Div(
                [
                    html.P("Leads count per state" ),
                    dcc.Graph(
                        id="no",
                       # style={"height": "90%", "width": "98%"},
                        figure=geomap(),
                        config=dict(displayModeBar=False),
                        style={'width':'100%', 'height':'100%'}
                    ),
                ],
                 style={'width':'50%', 'display': 'inline-block'}
            )
        ],
        className="row",
        style={'width': '100%', 'display': 'inline-block'}
    ),
    ]


    

#callbacks work everytime a value gets assigned presumably... the callback sets a watcher on that value and then...
#when the value is assigned to the corresponding function is called and the output variables specified get set
#in this case when we initialise dashboard2... tab_value gets set to display_tab, the callback in dashboard2 then
#returns the layout here... but we don't need to ever change what gets displayed in the map Graph, so we're good to 
#not have a callback here!
                
                
#layout on the page appears to be affected by stylesheets (that decide the width of divs with a given classname and such...)
#e.g. four columns chart_div appears to allow me to put three next to each other!
                
#can play with style= in divsand graphs to get stuff to fit... not really sure why there's so much whitespace around stuff but still