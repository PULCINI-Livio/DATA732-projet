import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from unidecode import unidecode

#Chemin des fichiers
file_path = 'data/liste-197-etats-2020.csv'

file_name = "data/fr.sputniknews.africa--20220630--20230630.json"

#Charger le fichier CSV en utilisant l'encodage ISO-8859-1 et le point-virgule comme délimiteur
df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')
#Sélectionner seulement les colonnes "NOM" et "CAPITALE"
df_pays_capitale = df[['NOM', 'CAPITALE']]

liste_pays = df_pays_capitale["NOM"]
liste_pays = [unidecode(pays) for pays in liste_pays]

#Afficher les premières lignes pour vérification
print(df_pays_capitale)



def trouver_pays_par_capitale(capitale):
    try:
        pays = df.loc[df_pays_capitale['CAPITALE'] == capitale, 'NOM'].iloc[0]
        return pays
    except IndexError:
        return "Capitale non trouvée"
    
def is_a_state(loc):
    return loc.capitalize() in df['NOM'].unique()

def is_a_capital(loc):
    return loc.capitalize() in df['CAPITALE'].unique()

def two_highest_occurences_of_states(loc_tab):
    res = {}
    for loc in loc_tab:
        if is_a_capital(loc):
            loc=trouver_pays_par_capitale(loc) # conversion de la capitale en son pays
        if is_a_state(loc):
            loc = unidecode(loc).capitalize() # normalisation
            if loc in res:
                res[loc] += 1
            else:
                res[loc] = 1

        # Trier le dictionnaire par ordre décroissant
        res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
        # Réduire le dictionnaire aux deux premières clés
        res = {k: res[k] for k in list(res.keys())[:2]}
    return res

# Fonction pour incrémenter NbLink pour deux pays donnés
def increment_link(df, pays1, pays2):
    # Vérifier si la ligne avec ces deux pays (dans cet ordre) existe déjà
    condition = ((df['Pays1'] == pays1) & (df['Pays2'] == pays2)) | ((df['Pays1'] == pays2) & (df['Pays2'] == pays1))
    
    if df[condition].empty:  # Si aucune ligne ne correspond, on ajoute une nouvelle ligne
        new_row = {"Pays1": pays1, "Pays2": pays2, "NbLink": 1}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:  # Si une ligne existe déjà, on incrémente le NbLink
        df.loc[condition, "NbLink"] += 1
    #print(df)
    return df

def cpt_link_btw_states(fileName: str):
    """Retourne un dataframe qui contient le nombre de lien entre pays

    Keyword arguments:
    fileName -- nom du fichier json
    Return: retourne un df
    """

    # Charger le fichier JSON      
    with open(file_name, 'r') as f:
        data = json.load(f)

    res = pd.DataFrame(columns=["Pays1", "Pays2", "NbLink"])
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
                            for i in range(len(data[year][month][day])-1):#on parcours chaque article
                                #on regarde les deux pays ayant le plus d'occurence (on compte aussi la capitale apr la suite)
                                #data[year][month][day][i]["loc"]
                                thoos = two_highest_occurences_of_states(data[year][month][day][i]["loc"])
                                two_highest = list(thoos.keys())
                                #print(two_highest)
                                if len(two_highest) > 1: #si au moins 2 pays sont cités
                                    if two_highest[0].lower() != two_highest[1].lower():
                                        res = increment_link(res, two_highest[0], two_highest[1])
                                #print(res)
                                    #### ensuite on incrémente le dataframe à la ligne qui contient les deux pays et nb_lien
                    #new_data = {"Nombre d'articles": cpt, "Date": year+"/"+month}
                    #res = pd.concat([res, pd.DataFrame([new_data])], ignore_index=True)

    return res.sort_values(by="NbLink", ascending=False)

"""df_link = cpt_link_btw_states(file_name)
#print(df_link.head(10))
# Sauvegarder un DataFrame en CSV
df_link.to_csv("link_nb_btw_states.csv", index=False)
mask = (df_link["Pays1"] == "Russie") | (df_link["Pays2"] == "Russie")
print(df_link[mask].head(10))
#pays_mentions = list(set(df_link['Pays1']).union(set(df_link['Pays2'])))
#pays_mentions.sort()
#print(len(pays_mentions))"""


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Pays mis le plus en liens'),
    dcc.Dropdown(
        id="dropdown",
        options= liste_pays,
        value="Russie",
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])

#columns=["Pays1", "Pays2", "NbLink"]

@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
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

#app.run_server(debug=True)
