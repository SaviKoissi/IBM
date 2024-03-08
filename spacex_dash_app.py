# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[ 
                     {'label': 'All Sites', 'value': 'ALL'}, 
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
])

# Function decorator to specify function input and output
# Function decorator to specify function input and output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # If all sites are selected, show overall success/failure pie chart
        fig = px.pie(spacex_df, names='class', title='Success Launches for All Sites')
    else:
        # If a specific site is selected, filter the DataFrame and show success/failure pie chart for that site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Success vs Failure for {entered_site}')

    return fig




# TASK 3: Add a slider to select payload range
# dcc.RangeSlider(id='payload-slider',...)
app.layout.children.append(dcc.RangeSlider(id='payload-slider',
                                           min=0, max=10000, step=1000,
                                           marks={0: '0', 100: '100'},
                                           value=[min_payload, max_payload]))

# TASK 4: Add a scatter chart to show the correlation between payload and launch success
app.layout.children.append(html.Div(dcc.Graph(id='success-payload-scatter-chart')))

# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Add a new scatter plot to show the correlation between Payload and Launch Outcome
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, selected_payload):
    # Filter DataFrame based on selected launch site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    # Filter DataFrame based on selected payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= selected_payload[0]) & (filtered_df['Payload Mass (kg)'] <= selected_payload[1])]

    # Create scatter plot
    scatter_fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Scatter plot for Payload and Launch Outcome ({selected_site if selected_site != "ALL" else "All Sites"})'
    )

    # Update layout for better visualization
    scatter_fig.update_layout(
        xaxis_title='Payload Mass (kg)',
        yaxis_title='Launch Outcome',
        legend_title='Booster Version Category'
    )

    return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server()
