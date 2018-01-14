import os
from time import time
from zipfile import ZipFile
from cryptoprovider import cryptocompare

# Limit of 4000 requests per hour. Total of 1992 coins when I wrote this code. So probably more now.


### Your parameters ###

# currency of reference
CURR = 'USD'
# List of coins (or dict of coins with codes as key)
coins = cryptocompare.get_meta()
# key in cryptocompare.FREQUENCY
freq = 'm'
# root directory
root = "data" #current directory/data



### Script ###

directory = f"{root}"
if not os.path.exists(directory):
    os.makedirs(directory)

with ZipFile(f"{directory}/{freq}.zip", mode='a')as zip:
    start = time()
    total = len(coins)
    i=1
    # print(len(zip.infolist()))
    print(f"Start downloading coins freq: {freq}")
    for coin in coins:
        print(f"{i}/{total}: {coin}")
        data = cryptocompare.get_historical_price(coin, limit=2000, toSymbol=CURR, frequency=freq)
        if not data.empty:
            zip.writestr(f"{coin}_{CURR}.csv", data.to_csv(index_label="time"))
        else:
            print(f"{coin} returns empty")
        i += 1
    print(f"It tooks {time()-start}s")
