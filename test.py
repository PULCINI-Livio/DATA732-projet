from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Exemple de DataFrame
data = {
    "pays": ["France", "Algérie", "Russie"],
    "Occurence": [2663, 1287, 8326],
    "code_iso": ["FRA", "DZA", "RUS"]
}
df = pd.DataFrame(data)

# Initialisation de l'application Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H4('Carte des occurrences par pays'),
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": pays, "value": code_iso} for pays, code_iso in zip(df["pays"], df["code_iso"])],
        value="FRA",
        clearable=False,
    ),
    dcc.Graph(id="map"),
])

@app.callback(
    Output("map", "figure"),
    [Input("dropdown", "value")]
)
def update_map(selected_country):
    # Créer une carte choroplèthe
    fig = px.choropleth(
        df,
        locations="code_iso",
        color="Occurence",
        hover_name="pays",
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    # Mettre en évidence le pays sélectionné
    fig.update_traces(
        marker_line_width=2,
        marker_line_color="black"
    )
    fig.update_layout(
        title="Occurrences par pays",
        geo=dict(showframe=False, showcoastlines=True),
    )
    return fig

@app.callback(
    Output("dropdown", "value"),
    [Input("map", "clickData")]
)
def update_dropdown_from_map(click_data):
    if click_data is not None:
        return click_data["points"][0]["location"]  # Renvoie le code_iso du pays cliqué
    return "FRA"  # Valeur par défaut

if __name__ == "__main__":
    app.run_server(debug=True)