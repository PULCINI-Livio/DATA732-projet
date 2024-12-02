from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from unidecode import unidecode

from nbOccurencesPaysParMois import *
from carteIntercative import *
from link_chart import *


#Chemin des fichiers
file_path = 'data/liste-197-etats-2020.csv'

file_name = "data/fr.sputniknews.africa--20220630--20230630.json"

#Charger le fichier CSV en utilisant l'encodage ISO-8859-1 et le point-virgule comme délimiteur
df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')
#Sélectionner seulement les colonnes "NOM" et "CAPITALE"
df_pays_capitale_code = df[['NOM', 'CAPITALE', 'CODE']]

liste_pays = df_pays_capitale["NOM"]
liste_pays = [unidecode(pays) for pays in liste_pays]

#Afficher les premières lignes pour vérification
#print(df_pays_capitale)



# Initialisation de l'application Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H4('Carte'),
    dcc.Dropdown(
        id="dropdown",
        options=liste_pays,
        value="Russie",
        clearable=False,
    ),
    dcc.Graph(id="map"),
    html.H4("Graphique des liens"),
    dcc.Graph(id="bar-chart"),
    html.H4("Graphique des occurences"),
    dcc.Graph(id="line-chart"),
])

# Callback pour mettre à jour la carte
@app.callback(
    Output("map", "figure"),
    [Input("dropdown", "value")]
)
def update_map(selected_country):
    # Créer une carte choroplèthe
    df = traitement()
    fig = px.choropleth(
        df,
        locations="code_iso",
        color="Occurence",
        hover_name="pays",
        color_continuous_scale=['#C1C5FD','#929AFC','#636EFA','#32377D']
    )
    # Mettre en évidence le pays sélectionné
    fig.update_traces(
        marker_line_width=1,
        marker_line_color="black"
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
        return click_data["points"][0]["hovertext"]  # Renvoie le code_iso du pays cliqué
    return "Russie"  # Valeur par défaut

# Callback pour mettre à jour le bar chart des liens
@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value")]
)
def update_bar_chart(pays):
    df = cpt_link_btw_states(file_name)
    df = df
    mask = (df["Pays1"] == pays) | (df["Pays2"] == pays)
    #inversion des pays pour ne mettre {pays} que dans la première colonne
    for index, row in df.iterrows():
        if row['Pays2'] == pays:
            # Échanger les valeurs de Pays1 et Pays2
            df.at[index, 'Pays1'], df.at[index, 'Pays2'] = df.at[index, 'Pays2'], df.at[index, 'Pays1']
    #df = df.head(10)
    fig = px.bar(df[mask], x="Pays2", y="NbLink")
    return fig


# Callback pour mettre à jour le bar chart des occurences
@app.callback(
    Output("line-chart", "figure"),
    [Input("dropdown", "value")]
)
def update_line_chart(pays):
    # Appeler creer_figure pour obtenir les données
    df = creer_figure(pays)
    
    # Vérifier si df est vide ou None
    if df is None or df.empty:
        print(f"Aucune donnée à afficher pour le pays : {pays}")
        return px.line(title="Aucune donnée disponible")
    
    # Appliquer le masque pour filtrer les données du pays
    mask = df["Pays"] == pays
    fig = px.line(
        df[mask], 
        x="Date_Pays", 
        y="Nombre d'articles", 
        title=f"Nombre d'articles pour {pays}", 
        markers=True  # Ajoute des points pour visualiser chaque donnée individuelle
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)