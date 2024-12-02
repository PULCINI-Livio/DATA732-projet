import json
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from unidecode import unidecode


file_name = "data/fr.sputniknews.africa--20220630--20230630.json"

# Chemin du fichier CSV
file_path = 'data/liste-197-etats-2020.csv'

# Charger le fichier CSV en utilisant l'encodage ISO-8859-1 et le point-virgule comme délimiteur
df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')
# Sélectionner seulement les colonnes "NOM" et "CAPITALE"
df_pays_capitale = df[['NOM', 'CAPITALE']]
# Lister les différents pays du monde
liste_pays = df_pays_capitale["NOM"]
liste_pays = [unidecode(pays) for pays in liste_pays]


# Afficher les premières lignes pour vérification
print(df_pays_capitale)
print('Russie' in df['NOM'].unique())


def occurencesParPays(fileName: str, pays: str):
    """Retourne un dataframe qui contient le nombre d'articles par mois pour un pays donné.

    Keyword arguments:
    fileName -- nom du fichier JSON
    pays -- le pays à rechercher
    Return: retourne un DataFrame
    """
    # Charger le fichier JSON
    with open(file_name, 'r') as f:
        data = json.load(f)

    res = pd.DataFrame(columns=["Pays", "Nombre d'articles", "Date"])
    data = data["data"]

    custom_order_year = ["2022", "2023"]
    custom_order_month = [str(i) for i in range(1, 13)]
    custom_order_day = [str(i) for i in range(1, 32)]

    for year in custom_order_year:
        if year in data:
            for month in custom_order_month:
                if month in data[year]:
                    for day in custom_order_day:
                        if day in data[year][month]:
                            for i in range(len(data[year][month][day]) - 1):
                                for location in data[year][month][day][i]["loc"]:
                                    if location in df_pays_capitale["NOM"].unique():
                                        date_str = f"{year}/{month}"

                                        # Filtrer le DataFrame des résultats pour trouver la correspondance
                                        existing_entry = res[
                                            (res["Pays"] == location) & (res["Date"] == date_str)
                                        ]

                                        if not existing_entry.empty:  # Vérifier si une entrée existe déjà
                                            # Si une entrée existe, incrémenter le nombre d'articles
                                            res.loc[existing_entry.index, "Nombre d'articles"] += 1
                                        else:
                                            # Ajouter une nouvelle entrée pour le pays et la date
                                            new_row = {
                                                "Pays": location,
                                                "Nombre d'articles": 1,  # Initialiser avec 1
                                                "Date": date_str,
                                            }
                                            res = pd.concat([res, pd.DataFrame([new_row])], ignore_index=True)

    return res




# Filtrer les lignes où le pays est "Russie"
#res_russie = occurencesParPays(file_name)[occurencesParPays(file_name)["Pays"] == "Russie"]

# Afficher les résultats
#print(res_russie)
#print(smartSearch(data, "2023", "5", "0", "org"))

def creer_figure(pays):
    # Appeler la fonction occurencesParPays pour obtenir le DataFrame
    df = occurencesParPays(file_name, pays)
    
    # Vérifier que le DataFrame n'est pas vide
    if df.empty:
        print(f"Aucune donnée trouvée pour le pays : {pays}")
        return pd.DataFrame()  # Retourne un DataFrame vide pour éviter les erreurs

    # Combiner Date et Pays pour créer une nouvelle colonne "Date_Pays"
    df["Date_Pays"] = df["Date"] 

    # Retourner le DataFrame
    return df

    
app = Dash(__name__)

app.layout = html.Div([
    html.H4('Fréquence articles par pays'),
    dcc.Dropdown(
        id="dropdown",
        options= liste_pays, 
        value="Russie",
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def update_bar_chart(pays):
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


app.run_server(debug=True)