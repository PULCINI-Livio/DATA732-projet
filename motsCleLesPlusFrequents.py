

import json
import pandas as pd
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



data = metaSearch(file_name,"0", "0", "0", "kws")

df = pd.DataFrame(columns=["Fréquence", 'Mot clé'])

# Parcourir les clés en fonction des valeurs décroissantes
for key in sorted(data, key=data.get, reverse=True)[:10]:
    #print(key, data[key])
    df.loc[len(df)] = [data[key], key]  # Ligne à l'index 1


fig = px.bar(df, x="Mot clé", y="Fréquence")
fig.show()
fig.write_html("motsCleLesPlusFrequents.html")




