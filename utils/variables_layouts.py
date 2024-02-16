import dash_bootstrap_components as dbc
from dash import dcc, html
import json
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))  # get directory path of file
PARENT_DIR = os.path.dirname(CURRENT_DIR)  # get parent directory path
sys.path.append(CURRENT_DIR)
import data_loader

with open(os.path.join(PARENT_DIR, 'Processed', 'rows_with_lower_export_frequent_structured.json'), 'r') as f:
    low_export_frequent = json.load(f)
with open(os.path.join(PARENT_DIR, 'Processed', 'rows_with_lower_export_frequent_structured_provinces.json'), 'r') as f:
    low_export_frequent_province = json.load(f)

# Layout 
# navbar
navbar = dbc.NavbarSimple(
    brand=html.H3('Trade Value Between Canadian Provinces and US States', style={'padding-left':50, 'color': '#3C577C', 'font': 'Poppins', 'font-style': 'bold'}),
    color='secondary',
    fluid=True # True: so that in particular, the contents of the navbar fill the available horizontal space
)

# Dropdowns
data_type_dropdown = dcc.Dropdown(
    id='data-type-dropdown',
    options=['Canadian domestic exports'],
    placeholder='Select Type',
    style={'width': 300}
)

origin = dcc.Dropdown(
    id='origin-dropdown',
    placeholder='Select Origin',
    style={'width': 300}
)
destination = dcc.Dropdown(
    id='destination-dropdown',
    placeholder='Select Destination',
    style={'width': 300}
)

destination2 = dcc.Dropdown(
    id='destination-dropdown2',
    placeholder='Select Destination',
    options=list(sorted(data_loader.totals['destination'].unique())),
    style={'width': 300}
)


industry = dcc.Dropdown(
    id='industry-dropdown',
    placeholder='Select Industry',
    style={'width': 650}
)


industry2 = dcc.Dropdown(
    id='industry-dropdown2',
    placeholder='Select Industry',
    style={'width': 600}
)

origin3 = dcc.Dropdown(
    id='origin-dropdown3',
    placeholder='Select Origin',
    options=list(sorted(low_export_frequent_province.keys())),
    style={'width': 300}
)

destination3 = dcc.Dropdown(
    id='destination-dropdown3',
    placeholder='Select Destination',
    style={'width': 300}
)

industry3 = dcc.Dropdown(
    id='industry-dropdown3',
    placeholder='Select Industry',
    style={'width': 600}
)


text_off_1 = html.Div([html.P("""
By selecting the origin, the destination and the industry, you will be provided by a graph which shows the
trade values of an industry or a product from an origin to a destination"""),
html.P("""Also, You can select the type of trendline to have a better understanding of the given graph and its trends."""),
html.P("""It is worth mentioning that the given value for each month shows the total trade value at the end of the month."""),
html.P("""Caution: Updating the graphs might take some time.""", style={'color': 'red'})
])
offcanvas_1 = html.Div(
    [
        dbc.Button(
            "Tips",
            id="butt-offcanvas_1",
            n_clicks=0,
            color='warning',
            # class_name= "text-light"
        ),
        dbc.Offcanvas(
            html.P(text_off_1),
            id="offcanvas_1",
            scrollable=True,
            title="About This Page",
            is_open=False,
            placement='end',
            style={"text-align": "justify"}
        ),
    ], style={'text-align': 'right'}
)

#  figure
trendline_options = {
                     "Exponentially-weighted moving average": ["ewm", dict(halflife=2)],                
                     "Ordinary Least Squares": ["ols", None],
                     "Locally Weighted Scatterplot Smoothing": ['lowess', None],
                     "Locally Weighted Scatterplot Smoothing-1": ['lowess', dict(frac=0.1)],
                     "rolling": ['rolling', dict(window=5)],
                     "rolling-gaussian": ['rolling', dict(window=5, win_type="gaussian", function_args=dict(std=2))],
                     "rolling-median": ['rolling', dict(function="median", window=5)],
                     "rolling-max": ['rolling', dict(function="max", window=5)],
                     "Expanding-mean": ["expanding", None],
                     "expanding-max": ['expanding', dict(function="max")],
                     }

trendline_dropdown = dcc.Dropdown(
    id='trendline-dropdown',
    options = list(trendline_options.keys()),
    value="Exponentially-weighted moving average",
    placeholder='Select Type of Trendline',
    style={'width': 400, 'backgroundColor': "#3EAEC6", "background-color":"#3EAEC6"}
)

# alert
alert2 = dbc.Alert(
            "Select all the options above to see recommendations",
            id="alert2",
            dismissable=True,
            fade=True,
            is_open=True,
            color='danger'
        )

alert3 = dbc.Alert(
            "Select all the options above to see recommendations",
            id="alert3",
            dismissable=True,
            fade=True,
            is_open=True,
            color='danger'
        )

# table
table_header2 = [
    html.Thead(html.Tr([html.Th("Date"), html.Th("Total Exports From All Countries ($)"), html.Th("Total Exports From Canada ($)")]))
]

table_body2 = [html.Tbody(children = [], id='table2')]

table2 = dbc.Table(table_header2 + table_body2, 
    bordered=True,
    dark=True,
    color="primary",
    hover=True,
    responsive=True,
    striped=False,)

list_group2 = dbc.ListGroup(
    [
        dbc.ListGroupItem(
            [
                html.Div(
                    [html.H5("Total Exports From All Countries ($)", className="mb-1")],
                    className="d-flex w-100 justify-content-between",
                ),
                # html.P("And some text underneath", className="mb-1"),
                html.Small(id= 'ave-total_2', className="text-info"),
                html.Br(),
                html.Small(id= 'max-total_2', className="text-info"),
                html.Br(),
                html.Small(id= 'min-total_2', className="text-info"),
            ]
        ),
        dbc.ListGroupItem(
            [
                html.Div(
                    [html.H5("Exports From Canada ($)", className="mb-1")],
                    className="d-flex w-100 justify-content-between",
                ),
                # html.P("And some text underneath", className="mb-1"),
                html.Small(id= 'ave-Ca_2', className="text-info"),
                html.Br(),
                html.Small(id= 'max-Ca_2', className="text-info"),
                html.Br(),
                html.Small(id= 'min-Ca_2', className="text-info"),
            ]
        ),
        
    ])

text_off_2 = html.Div([html.P("""
By selecting the destination and the industry, some suggestions for the proper 
months for exporting that product or industry to that destination will be given."""),
html.P("""This page suggests the best months for making a trade to a destination based on the 
average value of exports of the selected product to the selected destination from all countries 
and Canada. In other word, we consider the average value of exports from all countries to the destination 
within a period of time (e.g., 24 months) and find the periods that the export value is more than the average.
This shows that the demand in this period is higher than other times."""),
html.P("""Also, we find the months that the exports from Canada is lower than the average value of exports 
within this period of time. The intersections of these 2 analyses end in final result."""),
html.P("""It is worth mentionaing that this phenomenon should happen more than 1 time to consider it as a periodic event.
"""),
html.P("""Caution: updating the tables might take some time.""", style={'color': 'red'})
])
offcanvas_2 = html.Div(
    [
        dbc.Button(
            "Tips",
            id="butt-offcanvas_2",
            n_clicks=0,
            color='warning',
            # class_name= "text-light"
        ),
        dbc.Offcanvas(
            html.P(text_off_2),
            id="offcanvas_2",
            scrollable=True,
            title="About This Page",
            is_open=False,
            placement='end',
            style={"text-align": "justify"}
        ),
    ], style={'text-align': 'right'}
)



table_header3 = [
    html.Thead(html.Tr([html.Th("Date"), 
                        html.Th("Total Exports From All Countries ($)"), 
                        html.Th("Total Exports From Canada ($)"), 
                        html.Th(children = "Total Exports From origin ($)", id='table_header')]))
]

table_body3 = [html.Tbody(children = [], id='table3')]

table3 = dbc.Table(table_header3 + table_body3, 
    bordered=True,
    dark=True,
    color="primary",
    hover=True,
    responsive=True,
    striped=False,)


list_group3 = dbc.ListGroup(
    [
        dbc.ListGroupItem(
            [
                html.Div(
                    [html.H5("Total Exports From All Countries ($)", className="mb-1")],
                    className="d-flex w-100 justify-content-between",
                ),
                # html.P("And some text underneath", className="mb-1"),
                html.Small(id= 'ave-total_3', className="text-info"),
                html.Br(),
                html.Small(id= 'max-total_3', className="text-info"),
                html.Br(),
                html.Small(id= 'min-total_3', className="text-info"),
            ]
        ),
        dbc.ListGroupItem(
            [
                html.Div(
                    [html.H5("Exports From Canada ($)", className="mb-1")],
                    className="d-flex w-100 justify-content-between",
                ),
                # html.P("And some text underneath", className="mb-1"),
                html.Small(id= 'ave-Ca_3', className="text-info"),
                html.Br(),
                html.Small(id= 'max-Ca_3', className="text-info"),
                html.Br(),
                html.Small(id= 'min-Ca_3', className="text-info"),
            ]
        ),
        dbc.ListGroupItem(
            [
                html.Div(
                    [html.H5("Exports From Origin ($)", className="mb-1", id = 'origin-h5_3')],
                    className="d-flex w-100 justify-content-between",
                ),
                # html.P("And some text underneath", className="mb-1"),
                html.Small(id= 'ave-org_3', className="text-info"),
                html.Br(),
                html.Small(id= 'max-org_3', className="text-info"),
                html.Br(),
                html.Small(id= 'min-org_3', className="text-info"),
            ]
        ),
        
    ])


text_off_3 = html.Div([html.P("""
By selecting the origin, the destination and the industry, some suggestions for the proper 
months for exporting that product or industry to that destination from the selected origin will be given."""),
html.P("""This page suggests the best months for making a trade to a destination based on the 
average value of exports of the selected product to the selected destination from all countries 
and Canada. In other word, we consider the average value of exports from all countries and from Canada to the destination 
within a period of time (e.g., 24 months) and find the months that the export values are more than the average in both terms.
This shows that the demand in these months is higher than other times."""),
html.P("""Also, we find the months that the exports from the origin (e.g., Alberta) is lower than the average value of exports 
within this period of time. The intersections of these 3 items end in final result."""),
html.P("""It is worth mentionaing that this phenomenon should happen more than 1 time to consider it as a periodic event.
"""),
html.P("""Caution: updating the tables might take some time.""", style={'color': 'red'})
])
offcanvas_3 = html.Div(
    [
        dbc.Button(
            "Tips",
            id="butt-offcanvas_3",
            n_clicks=0,
            color='warning',
            # class_name= "text-light"
        ),
        dbc.Offcanvas(
            html.P(text_off_2),
            id="offcanvas_3",
            scrollable=True,
            title="About This Page",
            is_open=False,
            placement='end',
            style={"text-align": "justify"}
        ),
    ], style={'text-align': 'right'}
)