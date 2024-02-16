from dash import Dash, html, dcc, Input, Output, State, no_update, dash_table
import dash_bootstrap_components as dbc
from utils import variables_layouts as va_lay

tab3 = html.Div([
        #     html.Br(),
            va_lay.offcanvas_3,
            dbc.Row([dbc.Progress(value=0, id='progress-bar3', color="success", className="mb-3",style={"height": "1px"}),
                            html.Br()],style={'padding-left':0}),
            dbc.Row([
                    dbc.Col([html.H5('origin:'), va_lay.origin3]),
                    dbc.Col([html.H5('Destination:'), va_lay.destination3]),
                    dbc.Col([html.H5('Industry:'), va_lay.industry3]),
            ],style={'padding-left':50}),
            html.Br(),
            dbc.Col([va_lay.alert3], width=4, style={'padding-left':80}),
            html.Br(),
            dbc.Row([
                    dbc.Col([
                    html.H3(dbc.Badge(id='trade_badge3',children="", 
                                      color="#3C577C", text_color="#3C577C", className="ms-1"), style={'padding-left':80, 'width': '100%'})
                        ]),
                        dbc.Col([dbc.Row([],id='listgroup3', style={'padding-left':80}),])
            ],style={"background-color":"#C5F6FF"}),
            html.Br(),
            dbc.Row([
                dbc.Col([va_lay.table3], style={'padding-left': 80}),
                dbc.Col([va_lay.list_group3], width =3, style={'padding-right': 80})
            ])
])