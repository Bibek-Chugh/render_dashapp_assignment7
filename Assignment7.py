import os
import dash
from dash import dcc, html, Input, Output, callback
import numpy as np
import pandas as pd
import plotly.express as px



app = dash.Dash()
server = app.server
app.run_server(host='0.0.0.0', port=int(os.environment.get("PORT", 100000)))
cup_winners = {
    "Winners": [
        "Uruguay", "Italy", "Italy", "Uruguay", "Germany", "Brazil", "Brazil", "England", "Brazil", "Germany",
        "Argentina", "Italy", "Argentina", "Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany", "France", "Argentina"
    ],
    "Years": [
        [1930], [1934, 1938], [1934, 1938], [1950], [1954, 1974, 1990],
        [1958, 1962, 1970, 1994, 2002], [1958, 1962, 1970, 1994, 2002], [1966],
        [1958, 1962, 1970, 1994, 2002], [1954, 1974, 1990],
        [1978, 1986, 2022], [1934, 1938, 1982, 2006], [1978, 1986, 2022], [1954, 1974, 1990],
        [1958, 1962, 1970, 1994, 2002], [1998, 2018], [1958, 1962, 1970, 1994, 2002],
        [1934, 1938, 1982, 2006], [2010], [2014], [1998, 2018], [1978, 1986, 2022]
    ],
    "runner_ups": [
        "Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", "Sweden", "Czechoslovakia", "Germany", "Italy", "Netherlands",
        "Netherlands", "Germany", "Germany", "Argentina", "Italy", "Brazil", "Germany", "France", "Netherlands", "Argentina", "Croatia", "France"
    ]
}

# Create DataFrame
df = pd.DataFrame(cup_winners)

df_expanded = df.explode('Years')
# Combine all the years into a single string for each country
df['Years_combined'] = df['Years'].apply(lambda x: ', '.join(map(str, x)))

app.layout = html.Div([
    html.H1("FIFA World Cup Winners"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in sorted(df_expanded['Years'].unique())],
        placeholder="Select a year",
        clearable=True
    ),
    dcc.Graph(id='World Map')
])

@callback(
    Output('World Map', 'figure'),
    [Input('year-dropdown', 'value')]
)


def update_map(selected_year):
    filtered_df = df_expanded if not selected_year else df_expanded[df_expanded['Years'] == selected_year]
    
    fig = px.choropleth(
        filtered_df,
        locations="Winners",
        locationmode="country names",
        color="Winners",
        hover_name="Winners",
        hover_data={"Years": True, "runner_ups": True},
        color_continuous_scale="Viridis",
        scope="world",
        title=f"World Cup Winner for {selected_year}" if selected_year else "World Cup Winners"
    )
    return fig



app.run(debug=True)
