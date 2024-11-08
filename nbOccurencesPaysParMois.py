import json
import pandas as pd
import plotly.express as px

file_name = "fr.sputniknews.africa--20220630--20230630.json"

# Chemin du fichier CSV
file_path = 'liste-197-etats-2020.csv'

# Charger le fichier CSV en utilisant l'encodage ISO-8859-1 et le point-virgule comme délimiteur
df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';')
# Sélectionner seulement les colonnes "NOM" et "CAPITALE"
df_pays_capitale = df[['NOM', 'CAPITALE']]


# Afficher les premières lignes pour vérification
print(df_pays_capitale)
print('France' in df['NOM'].unique())


def occurencesParPays(fileName: str):
    """Retourne un dataframe qui contient le nombre d'article par mois

    Keyword arguments:
    fileName -- nom du fichier json
    Return: retourne un dictionnaire
    """

    # Charger le fichier JSON
    with open(file_name, 'r') as f:
        data = json.load(f)

    res = pd.DataFrame(columns=["Pays","Nombre d'articles", 'Date'])
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
                            for i in range(len(data[year][month][day])-1):
                                for location in data[year][month][day][i]["loc"]:
                                    if location in df_pays_capitale['NOM'].unique() : 
                                        if location in df_pays_capitale['NOM'].unique():
                                            date_str = f"{year}/{month}"

                                            # Filtrer le DataFrame des résultats pour trouver la correspondance
                                            existing_entry = res[(res["Pays"] == location) & (res["Date"] == date_str)]

                                            if not existing_entry.empty:
                                                # Si une entrée existe, incrémenter le nombre d'articles
                                                res.loc[existing_entry.index, "Nombre d'articles"] += 1
                                            else:
                                                # Ajouter une nouvelle entrée pour le pays et la date
                                                new_row = {"Pays": location, "Nombre d'articles": 1, "Date": date_str}
                                                res = pd.concat([res, pd.DataFrame([new_row])], ignore_index=True)

    return res


print(occurencesParPays(file_name))
# Filtrer les lignes où le pays est "Russie"
#res_russie = occurencesParPays(file_name)[occurencesParPays(file_name)["Pays"] == "Russie"]

# Afficher les résultats
#print(res_russie)
#print(smartSearch(data, "2023", "5", "0", "org"))

def creer_figure():
    # Appeler la fonction occurencesParPays pour obtenir le DataFrame
    df = occurencesParPays(file_name)
    
    # Combiner Date et Pays pour créer une nouvelle colonne "Date_Pays"
    df["Date_Pays"] = df["Date"] + " - " + df["Pays"]
    
    # Créer la figure en utilisant la colonne "Date_Pays" pour l'axe des x
    fig = px.bar(df, x="Date_Pays", y="Nombre d'articles",
                 labels={"Date_Pays": "Date et Pays", "Nombre d'articles": "Nombre d'articles"},
                 title="Nombre d'articles par mois et par pays")
    
    # Afficher et enregistrer la figure
    fig.show()
    fig.write_html("nombreArticlesParMois.html")

creer_figure()