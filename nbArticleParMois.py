import json
import pandas as pd
import plotly.express as px

file_name = "fr.sputniknews.africa--20220630--20230630.json"

def compteurNbArticleParMois(fileName: str):
    """Retourne un dataframe qui contient le nombre d'article par mois

    Keyword arguments:
    fileName -- nom du fichier json
    Return: retourne un dictionnaire
    """

    # Charger le fichier JSON
    with open(file_name, 'r') as f:
        data = json.load(f)

    res = pd.DataFrame(columns=["Nombre d'articles", 'Date'])
    data = data["data"]

    custom_order_year = ["2022", "2023"]
    custom_order_month = [str(i) for i in range(1, 13)]
    custom_order_day = [str(i) for i in range(1, 32)]   

    for year in custom_order_year:
        if year in data:
            for month in custom_order_month:
                if month in data[year]:
                    cpt=0
                    for day in custom_order_day:
                        if day in data[year][month]:
                            cpt += len(data[year][month][day])
                    new_data = {"Nombre d'articles": cpt, "Date": year+"/"+month}
                    res = pd.concat([res, pd.DataFrame([new_data])], ignore_index=True)

    return res

print(compteurNbArticleParMois(file_name))
#print(smartSearch(data, "2023", "5", "0", "org"))

def creer_figure():
    df = compteurNbArticleParMois(file_name)
    
    fig = px.bar(df, x="Date", y="Nombre d'articles")
    fig.show()
    fig.write_html("nombreArticlesParMois.html")

creer_figure()