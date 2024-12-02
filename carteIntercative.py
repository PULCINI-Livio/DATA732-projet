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
print(df_pays_capitale)
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
#on verra les capitale avec livio
def traitement():
    """
    fonction qui permet de traité les donnée du json pour pouvoir compté le nombre d'occurence 
    des pays en comptant le nombre d'apparition de son nom et celui de leur capitale 
    """
    for lieu in data["metadata"]["all"]["loc"]:#parcour des données
        if lieu in df['NOM'].unique() and is_a_state(lieu):
            
            df_Occurence.loc[len(df_Occurence)]=[lieu,data["metadata"]["all"]["loc"][lieu], df.loc[df['NOM'] == lieu, 'CODE'].iloc[0]]
        
    return df_Occurence
print(traitement())



# Créer la carte à bulles
fig = px.scatter_geo(df_Occurence, 
                     locations="code_iso", 
                     size="Occurence", # Définir la taille des bulles selon la population 
                       hover_name="pays",# Afficher le nom du pays au survol
                     size_max=30,  # Taille maximale des bulles
                     projection="natural earth",  # Projection de la carte
                     title="Carte à Bulles des Pays par Population")

# Afficher la carte
fig.show()


# rajouté le calcule avec les capitale 
# rajouté les code 3 lettre dans le df_Occurence 
# finir de faire la carte 
# rajouté les couleur par taille de nombre d'occurence 























