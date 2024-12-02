import pandas as pd 
import json
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

file_name = "fr.sputniknews.africa--20220630--20230630.json"
#Chemin du fichier CSV
file_path = 'liste-197-etats-2020.csv'


# Charger le fichier JSON
with open(file_name, 'r') as f:
    data = json.load(f)

#Charger le fichier CSV en utilisant l'encodage ISO-8859-1 et le point-virgule comme délimiteur
df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')
#Sélectionner seulement les colonnes "NOM" et "CAPITALE"
df_pays_capitale = df[['NOM', 'CAPITALE','CODE']]

#Afficher les premières lignes pour vérification

def trouver_pays_par_capitale(capitale):
    try:
        pays = df.loc[df_pays_capitale['Capitale'] == capitale, 'Pays'].iloc[0]
        return pays
    except IndexError:
        return "Capitale non trouvée"
    
def is_a_state(loc):
    return loc.capitalize() in df['NOM'].unique()

def is_a_capital(loc):
    return loc.capitalize() in df['CAPITALE'].unique()

df_Occurence=pd.DataFrame({'pays': [],'Occurence': [],'code_iso':[]})


""" for i in df_Occurence['pays']:#parcour de ma liste d'occurence
         if lieu in df['NOM'].unique():
                if is_a_state(lieu)  :
"""

def traitement():
    """
    fonction qui permet de traité les donnée du json pour pouvoir compté le nombre d'occurence 
    des pays en comptant le nombre d'apparition de son nom et celui de leur capitale 
    """
    for lieu in data["metadata"]["all"]["loc"]:#parcour des données
        if lieu in df['NOM'].unique() and is_a_state(lieu):
            
            df_Occurence.loc[len(df_Occurence)]=[lieu,data["metadata"]["all"]["loc"][lieu], df.loc[df['NOM'] == lieu, 'CODE'].iloc[0]]
        
    return df_Occurence

traitement()


# Créer la carte à bulles
#fig = px.scatter_geo(df_Occurence, 
#                     locations="code_iso", 
#                     size="Occurence", # Définir la taille des bulles selon la population 
#                       hover_name="pays",# Afficher le nom du pays au survol
#                     size_max=30,  # Taille maximale des bulles
#                     projection="natural earth",  # Projection de la carte
#                     title="Carte à Bulles des Pays par Population")

# Afficher la carte
#fig.show()


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
        options=[{"label": pays, "value": code_iso} for pays, code_iso in zip(df_Occurence["pays"], df_Occurence["code_iso"])],
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
        df_Occurence,
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





