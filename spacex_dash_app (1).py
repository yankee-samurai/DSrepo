# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                # Create the dropdown component
                                html.Div(dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                            {'label': 'All Sites', 'value': 'ALL'}
                                            ] + 
                                            [{'label': site, 'value': site} for site in launch_sites
                                            ],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                    )
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([
                                    dcc.RangeSlider(
                                    id='payload-slider',
                                    min = min_payload,
                                    max = max_payload,
                                    step = 1000,
                                    marks={i: f'{i}' for i in range(min_payload, max_payload+1, 1000)},
                                    value=[min_payload, max_payload]
                                    ),
                                ]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                                    
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Use all data for the pie chart
        fig = px.pie(spacex_df, names='Launch Site', title='Total Success Launches for All Sites')
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Success vs. Failed Launches for {selected_site}')
    
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
   [Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
    ]
    )
def update_output(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    else:
        filtered_df = spacex_df[ 
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1]) &
            (spacex_df['Launch Site'] == selected_site)
        ]
        # Use all data for the scatter plot
    fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class',
            color='Booster Version Category',
            title='Payload vs. Launch Success'
        )
    
    return fig
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run(debug=True)

# Run the app
if __name__ == '__main__':
    app.run_server()
