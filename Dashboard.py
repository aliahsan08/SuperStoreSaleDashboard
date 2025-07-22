import os
import dash
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

card =  dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(f"Total Sales (in $)"),
                    dbc.CardBody([
                        html.Br(),html.Div(id = 'sales-value'),html.Br()
                    ],id = 'total-sales')
                ],className="bg-dark text-white shadow-lg rounded mb-4,",style={'textAlign':'center'})
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader('Total Profit (in $)'),
                    dbc.CardBody([
                        html.Br(),html.Div(id = 'profit-value'),html.Br()
                    ],id='total-profit')
                ],className = "bg-light text-dark shadow-lg rounded mb-4",style={'textAlign':'center'})
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader('Highest Profiting State (in $)'),
                    dbc.CardBody([
                        html.Br(),html.Div(id = 'profiting-state'),html.Br()
                    ])
                ],style={
                    'textAlign':'center',
                    "backgroundColor": "#dbeafe",
                    "color": "#1e3a8a",
                    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
                    "borderRadius": "5px",
                    "marginBottom": "1.5rem"
                    })
            ),
    ])

app.layout = html.Div([
    navbar,
    html.Br(),html.Br(),
    card,
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
    ]),
    html.Br()
])
@app.callback(
    Output('map', 'figure'),
    Output('bar', 'figure'),
    Input('year-slider', 'value'),
    Input('dropdown', 'value')
)
def updateGraph(selected_year,figure_data):
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
        y = grouped_df[figure_data],
        title=f"SuperStore {figure_data} in {selected_year[0]} - {selected_year[1]} "
    )
    fig2.update_layout(
        plot_bgcolor='#d5ebf6',
        paper_bgcolor='#FFFFFF',
    )
    return fig,fig2

@app.callback(
    Output('sales-value', 'children'),
    Output('profit-value', 'children'),
    Output('profiting-state', 'children'),
    Input('year-slider', 'value'),
)
def updateValues(selected_year):
    filtered_df = df[(df['Year'] >= selected_year[0]) & (df['Year'] <= selected_year[1])]
    sales_df = filtered_df.groupby(['State'],as_index = False)['Sales'].sum()
    profit_df = filtered_df.groupby(['State'],as_index = False)['Profit'].sum()
    profiting_state = f"{profit_df.loc[profit_df['Profit'].idxmax(), 'State']}: {round(profit_df['Profit'].max(),2)}"

    return round(sales_df['Sales'].sum(),2),round(profit_df['Profit'].sum(),2),profiting_state


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug = False)
