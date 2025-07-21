import dash
import os
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('Superstore.csv')

year = df['Year'].unique()
app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])
navbar = dbc.NavbarSimple(
    brand="SuperStore Sales Analytics Dashboard",
    fluid=True,
)
app.layout = html.Div([
    navbar,
    html.Br(),
    dbc.Row([
        dbc.Label("Select Year Range",style={'textAlign':'center'}),
        dcc.RangeSlider(
            id='year-slider',
            min=min(year),
            max=max(year),
            value=[min(year), max(year)],
            step=1,
            marks={str(year1): str(year1) for year1 in year},
        )
    ],style={'width': '70%', 'margin': 'auto'}),
    html.Br(),
    dbc.Row([
        dbc.Label("Select Figure Data",style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='dropdown',
            options=['Sales','Profit'],
            value='Sales',
            clearable=False,
            style={'width': '30%', 'margin': 'auto'}
        )
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='map')
        ],width = 6),
        dbc.Col([
            dcc.Graph(id='bar')
        ],width = 6),
    ])
])
@app.callback(
    Output('map', 'figure'),
    Output('bar', 'figure'),
    Input('year-slider', 'value'),
    Input('dropdown', 'value')
)
def makeGraph(selected_year,figure_data):
    filtered_df = df[(df['Year'] >= selected_year[0]) & (df['Year'] <= selected_year[1])]
    grouped_df = filtered_df.groupby(['State','State Abbrev'],as_index = False)[figure_data].sum()
    fig = px.choropleth(
        grouped_df,
        locationmode='USA-states',
        locations= grouped_df['State Abbrev'],
        color=figure_data,
        hover_name="State",
        color_continuous_scale=px.colors.sequential.Blues,
        scope='usa',
        title=f"SuperStore {figure_data} in {selected_year[0]} - {selected_year[1]} "
    )

    fig2 = px.bar(
        grouped_df,
        x = 'State',
        y = grouped_df[figure_data]
    )
    return fig,fig2
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug = False)
