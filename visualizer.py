from dash import Dash, html, dcc, Input, Output, State, no_update, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import warnings
import plotly
# import time
from utils import variables_layouts as va_lay
from utils import functions as mf
from utils import data_loader
import tab1_html, tab2_html, tab3_html
plotly.io.json.config.default_engine = 'orjson'
warnings.filterwarnings("ignore")



# Initialize Dash app with external stylesheets and meta tags
app = Dash(external_stylesheets=[dbc.themes.FLATLY], meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Define app layout
app.layout = html.Div([
                dbc.Row(va_lay.navbar),  # Render navbar from external module
                # html.Br(),
                dbc.Tabs([
                    dbc.Tab(tab1_html.tab1, label="Graph"),  # Tab 1 with label "Graph"
                    dbc.Tab(tab2_html.tab2, label="Suggestion 1"),  # Tab 2 with label "Suggestion 1"
                    dbc.Tab(tab3_html.tab3, label="Suggestion 2"),  # Tab 3 with label "Suggestion 2"
                    ])
], style={'fontFamily': 'Puppins', 'font-size': 20})  # Apply custom styling

# ------------------------------------------------------------------------------------------------------
# Tab 1
# Callback to update dropdown options based on selected values
@app.callback(
    Output(component_id='origin-dropdown', component_property='options'),
    Output(component_id='destination-dropdown', component_property='options'),
    Output(component_id='industry-dropdown', component_property='options'),
    Input(component_id='data-type-dropdown', component_property='value'),
    Input(component_id='origin-dropdown', component_property='value'),
    Input(component_id='destination-dropdown', component_property='value')
)
def update_dropdowns(_type, selected_origin, selected_destination):
    # Filter DataFrame based on selected data type
    dff = data_loader.df[data_loader.df['data_type']==_type]
    df1 = dff
    # Filter DataFrame based on selected origin
    if selected_origin:
        df1 = df1[df1['origin'] == selected_origin]
    # Filter DataFrame based on selected destination
    if selected_destination:
        df1 = df1[df1['destination'] == selected_destination]
    
    # Return sorted unique options for dropdowns
    return sorted(dff['origin'].unique()), sorted(dff['destination'].unique()), sorted(df1['industry'].unique())

# Callback to toggle offcanvas
@app.callback(
    Output("offcanvas_1", "is_open"),
    Input("butt-offcanvas_1", "n_clicks"),
    State("offcanvas_1", "is_open"),
)
def toggle_offcanvas_1(n1, is_open):
    # Toggle offcanvas based on button click
    if n1:
        return not is_open
    return is_open

# Callback to update graph based on selected values
@app.callback(
    Output(component_id='line-Graph', component_property='figure'),
    Output(component_id='badge', component_property='children'),
    Output(component_id="collapse-trendline", component_property="is_open"),
    Output(component_id='progress-bar', component_property='value'),
    Input(component_id='data-type-dropdown', component_property='value'),
    Input(component_id='origin-dropdown', component_property='value'),
    Input(component_id='destination-dropdown', component_property='value'),
    Input(component_id='industry-dropdown', component_property='value'),
    Input(component_id='year-checklist', component_property='value'),
    Input(component_id='trendline', component_property='value'),
    Input(component_id='trendline-dropdown', component_property='value'),
)
def update_graph(_type, origin, destination, industry, years, trendline, selected_trendline):
    # Filter DataFrame based on selected criteria
    dff = data_loader.df[data_loader.df['data_type']==_type]
    dff=dff[dff['origin']==origin]
    dff=dff[dff['destination']==destination]
    dff=dff[dff['industry']==industry]
    dff = dff[dff['Year'].isin(years)]
    dff['date'] = pd.to_datetime(dff['date'])
    dff.sort_values(by='date', inplace=True) 
    pbar_value = mf.progress_bar(_type, origin, destination, industry)
    
    # Plot graph
    fig1 = px.line(data_frame=dff, x='date', y='value')
    
    # Plot trendline if selected
    if trendline:
        fig2 = px.scatter(data_frame=dff, x='date', y='value', 
                          trendline=va_lay.trendline_options[selected_trendline][0], 
                          trendline_color_override='#3EAEC6', trendline_scope='trace', 
                          trendline_options=va_lay.trendline_options[selected_trendline][1])
        trendlie_dropdown_state = True
    else:
        fig2 = px.scatter(data_frame=dff, x='date', y='value')
        trendlie_dropdown_state = False

    # Update figure traces and layout
    fig2.update_traces(marker=dict(size=12))
    fig1.update_traces(line=dict(width=3, color='#3C577C'))
    fig = go.Figure(data=fig1.data + fig2.data)
    fig.update_layout({
        'plot_bgcolor': '#cce6dc',
        'paper_bgcolor': 'azure',
        'xaxis_title':"Time",
        'yaxis_title':"Value ($)",
    })
    fig.update_xaxes(griddash='dot'),
    fig.update_yaxes(griddash='dot')
    
    # Return updated figure, badge text, trendline visibility, and progress bar value
    if not _type or not industry or not origin or not destination:
        return fig, [dbc.Spinner(), "  Select all the options above to see the graph..."], trendlie_dropdown_state, pbar_value
    return fig, f"{_type} of {industry} from {origin} to {destination}", trendlie_dropdown_state, pbar_value


# -------------------------------------------------------------------------------------------------------------------------------
# Tab 2
# Callback to update industry dropdown options based on selected destination
@app.callback(
    Output(component_id='industry-dropdown2', component_property='options'),
    Input(component_id='destination-dropdown2', component_property='value')
)
def update_dropdowns_tab2(selected_destination):
    # Update dropdown options based on selected destination
    if selected_destination:
        return list(sorted(data_loader.totals[data_loader.totals['destination'] == selected_destination]['industry'].unique()))
    return []

# Callback to toggle offcanvas
@app.callback(
    Output("offcanvas_2", "is_open"),
    Input("butt-offcanvas_2", "n_clicks"),
    State("offcanvas_2", "is_open"),
)
def toggle_offcanvas_2(n1, is_open):
    # Toggle offcanvas based on button click
    if n1:
        return not is_open
    return is_open

# Callback to update badge and progress bar
@app.callback(
    Output(component_id='alert2', component_property='is_open'),
    Output(component_id='progress-bar2', component_property='value'),
    Input(component_id='industry-dropdown2', component_property='value'),
    Input(component_id='destination-dropdown2', component_property='value')
)
def update_badge_tab2(selected_industry, selected_destination):
    # Update badge and progress bar based on selected industry and destination
    pbar_value = mf.progress_bar2(selected_destination, selected_industry)
    if selected_destination and selected_industry:
        return False, pbar_value
    return True, pbar_value

# Callback to update table and sidebar averages
@app.callback(
    Output(component_id='trade_badge2', component_property='children'),
    Output(component_id='listgroup2', component_property='children'),
    Output(component_id='table2', component_property='children'),
    Output(component_id='ave-total_2', component_property='children'),
    Output(component_id='max-total_2', component_property='children'),
    Output(component_id='min-total_2', component_property='children'),
    Output(component_id='ave-Ca_2', component_property='children'),
    Output(component_id='max-Ca_2', component_property='children'),
    Output(component_id='min-Ca_2', component_property='children'),
    Output(component_id='des_suggestions_2', component_property='children'),
    Input(component_id='destination-dropdown2', component_property='value'),
    Input(component_id='industry-dropdown2', component_property='value')
)
def update_tab2(selected_destination, selected_industry):
    # Update table and sidebar content based on selected destination and industry
    condition1 = selected_destination in va_lay.low_export_frequent.keys()
    table_content = []
    listgroups = []
    badge_text = "Based on our knowledge, it is proper to make trades in these months:"
    total_listgroup = ["Average: ", "Maximum: ", "Minimum: "]
    Ca_listgroup = ["Average: ", "Maximum: ", "Minimum: "]
    des_sugg_col = []
    listgroup_children = []
    suggestions = []
    
    # Check if destination and industry are in the stored data
    if condition1:
        condition2 = selected_industry in va_lay.low_export_frequent[selected_destination].keys()
    
    # If conditions are met, retrieve suggestions
    if condition1 and condition2:
        suggestions = va_lay.low_export_frequent[selected_destination][selected_industry]
        for m in suggestions:
            try:
                listgroups.append(dbc.ListGroupItem(f"{m}", color="success", style={'font-size':30}))
            except:
                pass
        listgroup_children = dbc.ListGroup(
            listgroups,
            horizontal=True,
        )
    
    # Iterate through years and months to populate table content
    for year in data_loader.years:
        for month in data_loader.months:
            try:
                _temp = data_loader.totals[
                    (data_loader.totals['destination']==selected_destination) & 
                    (data_loader.totals['origin']=='Total All Countries')]
                temp = _temp[
                    _temp['industry'] == selected_industry]
                _temp1 = data_loader.totals[
                    (data_loader.totals['destination']==selected_destination) & 
                    (data_loader.totals['origin']=='Sub-Total')]
                temp1 = _temp1[
                    _temp1['industry'] == selected_industry]
                try:
                    out = temp[' '.join([year, month])].to_list()[0]
                    out1 = temp1[' '.join([year, month])].to_list()[0]
                    if month in suggestions:
                        table_content.append(html.Tr([html.Td(f"{' '.join([year, month])}"), html.Td(f"{out}"), html.Td(f"{out1}")], style={'color': '#18BC9C'}))
                    else:
                        table_content.append(html.Tr([html.Td(f"{' '.join([year, month])}"), html.Td(f"{out}"), html.Td(f"{out1}")]))
                except:
                    pass
            except:
                pass
    
    # Calculate and format average, max, and min values for total and CA
    try:    
        total_listgroup = [f"Average: {temp[data_loader.dates].mean(axis=1).to_list()[0]}", 
                            f"Max: {temp[data_loader.dates].max(axis=1).to_list()[0]}", 
                            f"Min: {temp[data_loader.dates].min(axis=1).to_list()[0]}"]
        Ca_listgroup = [f"Average: {temp1[data_loader.dates].mean(axis=1).to_list()[0]}", 
                        f"Max: {temp1[data_loader.dates].max(axis=1).to_list()[0]}", 
                        f"Min: {temp1[data_loader.dates].min(axis=1).to_list()[0]}"]
    except:
        pass
    
    # Generate suggested destination list for sidebar
    des_sugg_col = [dbc.Badge(children='Suggested destinations (in order):', 
                                color="#3C577C", text_color="#3C577C", className="ms-2", style={'text-align': 'left'})]
    des_sugg, month_sugg = mf.find_top_5(data_loader.totals, selected_industry, data_loader.dates)
    listgroups_2_1 = []
    for i in range(len(des_sugg)):
        listgroups_2_1.append(
            dbc.ListGroupItem(
                [
                    html.Div(
                        [
                            html.H5(f"{des_sugg[i]}", className="mb-1"),
                            html.Small(f"{i+1}", className="text-info"),
                        ],
                        className="d-flex w-100 justify-content-between",
                    ),
                    dbc.ListGroup([dbc.ListGroupItem(f"{n}", color="success", style={'font-size':20}) for n in month_sugg[i]], horizontal=True),
                ]
    ))
    des_sugg_col.append(dbc.ListGroup(
        listgroups_2_1,
        horizontal=False,
    ))
    
    return badge_text, listgroup_children, table_content, *total_listgroup, *Ca_listgroup, des_sugg_col

# -------------------------------------------------------------------------------------------------------------------------------
# tab3
# Callback to update destination and industry dropdown options based on selected origin and destination
@app.callback(
    Output(component_id='destination-dropdown3', component_property='options'),
    Output(component_id='industry-dropdown3', component_property='options'),
    Input(component_id='origin-dropdown3', component_property='value'),
    Input(component_id='destination-dropdown3', component_property='value'),
)
def update_dropdowns3(selected_origin, selected_destination):
    # Initialize empty lists to store options
    destinations = []
    industries = []
    
    # If both origin and destination are selected, update dropdown options
    if selected_origin and selected_destination:
        destinations = sorted(list(va_lay.low_export_frequent_province[selected_origin].keys()))
        industries = sorted(list(va_lay.low_export_frequent_province[selected_origin][selected_destination].keys()))

    # If only origin is selected, update destination dropdown options
    if selected_origin:
        destinations = sorted(list(va_lay.low_export_frequent_province[selected_origin].keys()))
     
    return destinations, industries

# Callback to toggle offcanvas
@app.callback(
    Output("offcanvas_3", "is_open"),
    Input("butt-offcanvas_3", "n_clicks"),
    State("offcanvas_3", "is_open"),
)
def toggle_offcanvas_3(n1, is_open):
    # Toggle offcanvas based on button click
    if n1:
        return not is_open
    return is_open

# Callback to update alert and progress bar
@app.callback(
    Output(component_id='alert3', component_property='is_open'),
    Output(component_id='progress-bar3', component_property='value'),
    Input(component_id='origin-dropdown3', component_property='value'),
    Input(component_id='destination-dropdown3', component_property='value'),
    Input(component_id='industry-dropdown3', component_property='value'),
)
def update_bar_alert_tab3(selected_origin, selected_destination, selected_industry):
    # Update alert and progress bar based on selected origin, destination, and industry
    pbar_value = mf.progress_bar3(selected_origin, selected_destination, selected_industry)
    if selected_destination and selected_industry and selected_origin:
        return False, pbar_value
    return True, pbar_value

# Callback to update badge and table
@app.callback(
    Output(component_id='trade_badge3', component_property='children'),
    Output(component_id='listgroup3', component_property='children'),
    Output(component_id='table3', component_property='children'),
    Output(component_id='table_header', component_property='children'),
    Output(component_id='ave-total_3', component_property='children'),
    Output(component_id='max-total_3', component_property='children'),
    Output(component_id='min-total_3', component_property='children'),
    Output(component_id='ave-Ca_3', component_property='children'),
    Output(component_id='max-Ca_3', component_property='children'),
    Output(component_id='min-Ca_3', component_property='children'),
    Output(component_id='ave-org_3', component_property='children'),
    Output(component_id='max-org_3', component_property='children'),
    Output(component_id='min-org_3', component_property='children'),
    Input(component_id='origin-dropdown3', component_property='value'),
    Input(component_id='destination-dropdown3', component_property='value'),
    Input(component_id='industry-dropdown3', component_property='value')
)
def update_badge_table3(selected_origin, selected_destination, selected_industry):
    # Initialize default values
    origin_table_header = f"Total Exports From origin ($)"
    spinner  = html.Td(dbc.Spinner(color="secondary"))
    badge_text = "Based on our knowledge, it is proper to make trades in these months:"
    total_listgroup = ["Average: ", "Maximum: ", "Minimum: "]
    Ca_listgroup = ["Average: ", "Maximum: ", "Minimum: "]
    origin_listgroup = ["Average: ", "Maximum: ", "Minimum: "]
    
    # Update origin table header if origin is selected
    if selected_origin:
        origin_table_header = f"Total Exports From {selected_origin} ($)"
    
    table_body = []
    listgroups = []
    
    # If all options are selected, update badge, list group, and table
    if selected_origin and selected_destination and selected_industry:
        suggestions = va_lay.low_export_frequent_province[selected_origin][selected_destination][selected_industry]
        for m in suggestions:
            listgroups.append(dbc.ListGroupItem(f"{m}",color="success", style={'font-size':30}))
        listgroup_children = dbc.ListGroup(
            listgroups,
            horizontal=True,
        )
        for year in data_loader.years:
            for month in data_loader.months:
                try:
                    _temp = data_loader.totals[
                        (data_loader.totals['destination']==selected_destination) & 
                        (data_loader.totals['origin']=='Total All Countries')]
                    temp = _temp[
                        _temp['industry'] == selected_industry]
                    _temp1 = data_loader.totals[
                        (data_loader.totals['destination']==selected_destination) & 
                        (data_loader.totals['origin']=='Sub-Total')]
                    temp1 = _temp1[
                        _temp1['industry'] == selected_industry]

                    _temp2 = data_loader.df2[
                        (data_loader.df2['destination']==selected_destination) & 
                        (data_loader.df2['origin']==selected_origin)
                    ]
                    temp2 = _temp2[
                        _temp2['industry'] == selected_industry]
                    try:
                        # to ignore not valid data like 2023 Aug which is not available in the dataset
                        out = temp[' '.join([year, month])].to_list()[0]
                        out1 = temp1[' '.join([year, month])].to_list()[0]
                        out2 = temp2[' '.join([year, month])].to_list()[0]
                        if month in suggestions:
                            table_body.append(html.Tr([html.Td(f"{' '.join([year, month])}"), html.Td(f"{out}"), html.Td(f"{out1}"), html.Td(f"{out2}")], 
                                                      style={'color': '#18BC9C'}))
                        else:
                            table_body.append(html.Tr([html.Td(f"{' '.join([year, month])}"), html.Td(f"{out}"), html.Td(f"{out1}"), html.Td(f"{out2}")]))
                    except:
                        out = 0
                except:
                    pass
        total_listgroup = [f"Average: {temp[data_loader.dates].mean(axis=1).to_list()[0]}", 
                           f"Max: {temp[data_loader.dates].max(axis=1).to_list()[0]}", 
                           f"Min: {temp[data_loader.dates].min(axis=1).to_list()[0]}"]
        Ca_listgroup = [f"Average: {temp1[data_loader.dates].mean(axis=1).to_list()[0]}", 
                        f"Max: {temp1[data_loader.dates].max(axis=1).to_list()[0]}", 
                        f"Min: {temp1[data_loader.dates].min(axis=1).to_list()[0]}"]
        origin_listgroup = [f"Average: {temp2[data_loader.dates].mean(axis=1).to_list()[0]}", 
                            f"Max: {temp2[data_loader.dates].max(axis=1).to_list()[0]}", 
                            f"Min: {temp2[data_loader.dates].min(axis=1).to_list()[0]}"]
        
        return badge_text, listgroup_children, table_body, origin_table_header, *total_listgroup, *Ca_listgroup, *origin_listgroup
    table_body = html.Tr([spinner, spinner, spinner, spinner])
    return '',[], table_body, origin_table_header, *total_listgroup, *Ca_listgroup, *origin_listgroup

app.run_server(debug=False)


