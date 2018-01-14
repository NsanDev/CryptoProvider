from zipfile import ZipFile
from pandas import read_csv, DataFrame
from io import StringIO


### Script to read data from zip

# Limit of 4000 requests per hour. Total of 1923 coins
CURR = 'USD'

freq = 'd'
# root directory
root = "data" #current directory/data


directory = f"{root}"
with ZipFile(f"{directory}/{freq}.zip", mode='r')as zip:
    # data_dict = {coin: read_csv(StringIO(zip.read(f"{coin}_{CURR}.csv").decode()), index_col=0, parse_dates=True)["close"] for coin in kraken_meta}
    data = read_csv(StringIO(zip.read(f"BTC_USD.csv").decode()), index_col=0)

# data = DataFrame(data_dict)
prices = data['2017-12-15':]