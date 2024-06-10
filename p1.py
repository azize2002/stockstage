import datetime as dt 
import pandas as pd 

from pandas_datareader import data as pdr 
# //1 data mnin jeyya


end=dt.datetime.now()    
# //datelyoum
start=dt.timedelta(2002,1,1) 
# //datemnin nabdew nshoufou
print(start,end)   


# //2 level up ==> on va importer quelques stocks et tickers (dans des listes)
# // yahoo tickers require ".AX" to be specified at the end of the ticker symbol for australian stocks

stocklist=["CBA","NAB","WBC"]
stocks=[i +'.AX' for i in stocklist]
print(stocks)

# //3 appel de pandass_datareader module 

dataframe = pdr.get_data_yahoo(stocks,start,end)
dataframe.head()

# //pour clarifier les donnes on peut utiliser index/columns/describe
dataframe.index 

# //faire une courbe avec plot 
df.plot()
 plt.title('Adjusted Close Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()



