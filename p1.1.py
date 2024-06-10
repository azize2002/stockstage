import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

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

# Vérification si des données ont été récupérées
if all_data.empty:
    print("No data retrieved")
else:
    # Affichage des premières lignes des données
    print(all_data.head(15))

    # Tracé des données
    plt.figure(figsize=(10, 6))
    for stock in stocks:
        stock_data = all_data[all_data['Ticker'] == stock]
        plt.plot(stock_data.index, stock_data['Adj Close'], label=stock)
    plt.title('Adjusted Close Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
