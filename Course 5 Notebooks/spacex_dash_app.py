# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
options = [{'label': 'All Sites', 'value': 'ALL'}]
options += [{'label' : val, 'value' : val} for val in spacex_df['Launch Site'].unique()]
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                             options=options,
                                             value='ALL',
                                             placeholder="Choose Site to Display",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10_000, step=1000,
                                                marks={0 : "0", 100: "100"},
                                                value=[0,10_000]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id="success-pie-chart",component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.copy() 
    if entered_site == 'ALL': 
        fig = px.pie(filtered_df, 
                 values="class",
                 names="Launch Site",
                 title ="Sucess Vs Failure for All Sites"
                 )
    else: 
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site].groupby(['Launch Site', 'class']).size().reset_index(name='class_count')
        fig = px.pie(filtered_df, 
               values="class_count", 
               names='class', 
               title=f'Total Successful Lauches for Site: {entered_site}')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')
)
def get_scatter_plot(entered_site, payload): 
    # The following will filter the dataframe for the values that are wanted based of the payload range selected
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    if entered_site == 'ALL': 
        fig = px.scatter(filtered_df, 
                 x='Payload Mass (kg)',
                 y="class",
                 color='Booster Version Category',
                 title ="Sucess Vs Failure for All Sites"
                 )
    else: 
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, 
                x='Payload Mass (kg)',
                y="class",
                color='Booster Version Category',
                title=f'Total Successful Lauches for Site: {entered_site}'
                )
    return fig
    

# Run the app
if __name__ == '__main__':
    app.run_server()
