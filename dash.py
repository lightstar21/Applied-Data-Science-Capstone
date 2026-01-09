# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Calculate min and max payload for the slider
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    html.Br(),
    
    # TASK 1: Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',  # default value
        placeholder="Select a Launch Site",
        searchable=True
    ),
    
    html.Br(),
    
    # TASK 2: Pie chart for success count
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    html.Br(),
    html.P("Payload range (Kg):"),
    
    # TASK 3: Payload range slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={
            0: '0 kg',
            2000: '2000 kg',
            4000: '4000 kg',
            6000: '6000 kg',
            8000: '8000 kg',
            10000: '10000 kg'
        }
    ),
    
    html.Br(),
    
    # TASK 4: Scatter plot for payload vs success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches By Site'
        )
        return fig
    else:
        # Filter for selected site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        
        fig = px.pie(
            site_df,
            names='class',
            title=f'Success vs Failure for site {entered_site}',
            color_discrete_map={0: '#ff4444', 1: '#44ff44'}  # red=failure, green=success
        )
        return fig


# TASK 4: Callback for scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    
    # Apply payload range filter
    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
        (filtered_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Sites',
            hover_data=['Launch Site', 'Booster Version Category'],
            labels={'class': 'Mission Outcome (0 = Failure, 1 = Success)'}
        )
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Success for {entered_site}',
            hover_data=['Booster Version Category'],
            labels={'class': 'Mission Outcome (0 = Failure, 1 = Success)'}
        )
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)