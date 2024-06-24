import datetime as dt
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine

# Dates de début et de fin pour les données
end = dt.datetime.now()
start = dt.datetime(2002, 1, 1)

print("Start Date:", start)
print("End Date:", end)

# Liste des actions à récupérer
stocklist = ["CBA", "NAB", "WBC"]
stocks = [i + '.AX' for i in stocklist]
print("Stocks:", stocks)

# Initialisation d'une liste pour stocker les DataFrames
dataframes = []

# Récupération des données pour chaque action individuellement
for stock in stocks:
    try:
        data = yf.download(stock, start=start, end=end)
        data['Ticker'] = stock  # Ajout d'une colonne pour identifier le ticker
        dataframes.append(data)
    except Exception as e:
        print(f"Error retrieving data for {stock}: {e}")

# Concatenation des DataFrames en un seul
if dataframes:
    all_data = pd.concat(dataframes)
else:
    all_data = pd.DataFrame()

# Transformation des données pour correspondre aux colonnes name, value
if not all_data.empty:
    all_data.reset_index(inplace=True)  # Réinitialisation de l'index pour obtenir la colonne 'Date'
    all_data.rename(columns={'Ticker': 'name', 'Close': 'value'}, inplace=True)  # Renommer les colonnes
    all_data = all_data[['name', 'value']]  # Sélection des colonnes pertinentes

# Fonction de nettoyage des chaînes de caractères pour l'encodage UTF-8
def encode_utf8(value):
    if isinstance(value, str):
        return value.encode('utf-8', 'ignore').decode('utf-8')
    return value

# Appliquer l'encodage aux colonnes de type chaîne de caractères
all_data['name'] = all_data['name'].apply(encode_utf8)

# Vérification des données avant insertion
print("Data to be inserted:")
print(all_data.head())
print(all_data.info())

# Connexion à la base de données PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:mahmoud2002@localhost:5432/mydatabase')

# Insertion des données dans la table stocks
try:
    all_data.to_sql('stocks', engine, if_exists='append', index=False)
    print("Data inserted successfully")
except Exception as e:
    print(f"Error inserting data into PostgreSQL: {e}")

# Vérification des données après insertion
try:
    with engine.connect() as connection:
        result = connection.execute('SELECT * FROM stocks')
        print("Data in the table after insertion:")
        for row in result:
            print(row)
except Exception as e:
    print(f"Error fetching data from PostgreSQL: {e}")
