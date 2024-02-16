from dash import Dash, html, dcc, Input, Output, State, no_update, dash_table
import dash_bootstrap_components as dbc
from utils import variables_layouts as va_lay

tab2 = html.Div([
        #     html.Br(),
            va_lay.offcanvas_2,
            dbc.Row([dbc.Progress(value=0, id='progress-bar2', color="success", className="mb-3",style={"height": "1px"}),
                            html.Br()],style={'padding-left':0}),
            dbc.Row([
                    dbc.Col([html.H5('Destination:'), va_lay.destination2]),
                    dbc.Col([html.H5('Industry:'), va_lay.industry2]),
            ],style={'padding-left':50}),
            html.Br(),
            dbc.Col([va_lay.alert2], width=4, style={'padding-left':80}),
            html.Br(),
            dbc.Row([
                    dbc.Col([
                    html.H3(dbc.Badge(id='trade_badge2',children="", 
                                      color="#3C577C", text_color="#3C577C", className="ms-1"), style={'padding-left':80, 'width': '100%'})
                        ]),
                        dbc.Col([dbc.Row([],id='listgroup2', style={'padding-left':80}),])
            ],style={"background-color":"#C5F6FF"}),
            html.Br(),
            dbc.Row([
                # dbc.Col([], width=2),
                dbc.Col([va_lay.table2], style={'padding-left': 80}),
                dbc.Col([va_lay.list_group2,
                         html.Br(),
                         html.Div(id='des_suggestions_2')], width =3, style={'padding-right': 80})
            ])
])