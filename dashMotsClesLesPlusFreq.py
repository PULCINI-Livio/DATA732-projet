import json
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

file_name = "fr.sputniknews.africa--20220630--20230630.json"


def metaSearch(fileName:str, year:str="0", month:str="0", day:str="0", category:str="all"):
    """Retourne un dictionnaire contenant les donnees demandees en parametre\n
        L'ordre des paramètres compte; si month=0 alors day=0 aussi mais pas pour year
    Keyword arguments:\n
    year -- l'année souhaitée, mettre 0 pour toutes les années\n
    month -- le mois souhaité, mettre 0 pour tous les mois\n
    day -- le jour souhaité, mettre 0 pour tous les jours\n
    category -- la catégory souhaité, -all- par défaut\n

    Return: dictionnaire
    """

    # Charger le fichier JSON
    with open(file_name, 'r') as f:
        data = json.load(f)

    res = []
    allData = False
    # Init d'un booléen pour savoir si on veut tout les types de données
    if category == "all":
        allData = True


    if year == "0": # Si pas d'année précisée
        if allData: # Si on veut tout les type de données
            res = data["metadata"]["all"]
        else:
            res = data["metadata"]["all"][category]
        
    elif month == "0": # Si pas de mois précisée, juste l'année
        if allData: # Si on veut tout les type de données
            res = data["metadata"]["year"][year]
        else:
            res = data["metadata"]["year"][year][category]

    elif day == "0": # Si pas de jour précisée, juste l'année et le mois
        if allData: # Si on veut tout les type de données
            res = data["metadata"]["month"][year][month]
        else:
            res = data["metadata"]["month"][year][month][category]

    else: # Si l'année, le mois et le jour sont précisés
        if allData: # Si on veut tout les type de données
            res = data["metadata"]["day"][year][month][day]
        else:
            res = data["metadata"]["day"][year][month][day][category]
        
    return res



def anneeFreqKW(file_name: str):
    df = pd.DataFrame(columns=['year', 'keywords', 'frequence'])
    years = ["2022", "2023"]

    for year in years:
        data = metaSearch(file_name, year, "0", "0", "kws")
        # Parcourir les clés en fonction des valeurs décroissantes
        for key in sorted(data, key=data.get, reverse=True)[:10]:
            # Utiliser un index unique en combinant l'année et l'index
            df.loc[len(df)] = [year, key, data[key]]  # Ajoute une nouvelle ligne à la fin

    return df


#print(AnneeFreqKW(file_name))



app = Dash(__name__)

app.layout = html.Div([
    html.H4('Mots clés les plus fréquents'),
    dcc.Dropdown(
        id="dropdown",
        options=["2022", "2023"],
        value="2022",
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def update_bar_chart(year):
    df = anneeFreqKW(file_name)
    mask = df["year"] == year
    fig = px.bar(df[mask], x="keywords", y="frequence", 
                barmode="group")
    return fig

app.run_server(debug=True)