from dash import Dash, html, dcc, Input, Output, State, no_update, dash_table
import dash_bootstrap_components as dbc
from utils import variables_layouts as va_lay
from utils import data_loader

tab1 = html.Div([
        # html.Br(),
        va_lay.offcanvas_1,
        dbc.Row([dbc.Progress(value=0, id='progress-bar', color="success", className="mb-3", style={"height": "2px"}),
                    html.Br()]),
        dbc.Row([     
                dbc.Col([html.H5('Type:'),va_lay.data_type_dropdown], width=2),
                dbc.Col([html.H5('Origin:'), va_lay.origin],width=2),
                dbc.Col([html.H5('Destination:'), va_lay.destination],width=2),
                dbc.Col([html.H5('Industry:'), va_lay.industry],width=3),
                ],style={'padding-left':50}
            ),
        html.Br(),
        dbc.Row([
            dbc.Col(
            dbc.Checklist(id='year-checklist', options = data_loader.df['Year'].unique(), value=data_loader.df['Year'].unique(), switch=True, 
                    style={'padding-left':50, 'fontSize': 20}, inline=True)),
            dbc.Col([
                dbc.Checklist(id='trendline', options = ['Trendline'], value=['Trendline'], switch=True, 
                    style={'fontSize': 20}, inline=True, 
                    input_checked_style={
                            "backgroundColor": "#3EAEC6",
                            "borderColor": "#3EAEC6",
                        }),
                dbc.Collapse(
                    va_lay.trendline_dropdown,
                    id="collapse-trendline",
                    is_open=False,
                    style={'fontSize': 18})
                ])
            ]),
        html.Br(),
        dbc.Row([
            html.H3(dbc.Badge(id='badge',children="", color="#3C577C", text_color="#3C577C", className="ms-1"), style={'padding-left':80, 'width': '100%'}),   
            dcc.Graph(id='line-Graph', responsive=True)
            ]),
    ],       
    style={'fontFamily':'Puppins'}
)