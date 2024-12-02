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

# Exemple de données pour un autre graphique (bar chart par pays)
data_bar = {
    "pays": ["France", "Algérie", "Russie"],
    "keywords": [["mot1", "mot2", "mot3"], ["mot4", "mot5"], ["mot6", "mot7", "mot8"]],
    "frequence": [[10, 20, 30], [15, 25], [35, 40, 50]],
}
df_bar = pd.DataFrame(data_bar)

# Initialisation de l'application Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H4('Carte et graphiques interactifs'),
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": pays, "value": code_iso} for pays, code_iso in zip(df["pays"], df["code_iso"])],
        value="FRA",
        clearable=False,
    ),
    dcc.Graph(id="map"),
    html.H4("Graphique des mots clés"),
    dcc.Graph(id="bar-chart"),
])

# Callback pour mettre à jour la carte
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
    fig.update_layout(
        title="Occurrences par pays",
        geo=dict(showframe=False, showcoastlines=True),
    )
    return fig

# Callback pour mettre à jour le dropdown à partir de la carte
@app.callback(
    Output("dropdown", "value"),
    [Input("map", "clickData")]
)
def update_dropdown_from_map(click_data):
    if click_data is not None:
        return click_data["points"][0]["location"]  # Renvoie le code_iso du pays cliqué
    return "FRA"  # Valeur par défaut

# Callback pour mettre à jour le bar chart
@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value")]
)
def update_bar_chart(selected_country):
    # Extraire le pays à partir du code ISO
    selected_pays = df[df["code_iso"] == selected_country]["pays"].values[0]
    
    # Filtrer les données pour le graphique en barre
    data_for_country = df_bar[df_bar["pays"] == selected_pays]
    keywords = data_for_country["keywords"].values[0]
    frequence = data_for_country["frequence"].values[0]
    
    # Créer le graphique en barre
    fig = px.bar(
        x=keywords,
        y=frequence,
        labels={"x": "Mots clés", "y": "Fréquence"},
        title=f"Mots clés pour {selected_pays}"
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
