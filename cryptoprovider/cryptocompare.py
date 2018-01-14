import requests as _requests
from json import loads as _loads
from pandas import DataFrame as _DataFrame, to_datetime as _to_datetime

# API
_URL_CRYPTOCOMPARE = 'https://min-api.cryptocompare.com/data'

# DEFAULTS
_CURR = 'EUR'


def get_meta():
    '''
    :return: available coins and meta_info
    '''
    url = 'https://www.cryptocompare.com/api/data/coinlist/'
    rawdata = _requests.get(url).content.decode()
    parseddata = _loads(rawdata)
    return parseddata['Data']


def get_kraken_coin():
    '''
    :return: dict of coins in meta_kraken.json
    '''
    with open(f'meta_kraken.json','r') as file:
        content = file.read()
        return _loads(content)

def get_price(fromSymbols, toSymbols):
    '''
    :return: current price of fromSymbols given in toSymbols. You can concat. for example: fromSymbols='ETH,ETC', toSymbols='USD,EUR'
    '''
    url = f"{_URL_CRYPTOCOMPARE}/pricemulti?fsyms={fromSymbols}&tsyms={toSymbols}"
    rawdata = _requests.get(url).content.decode()
    parseddata = _loads(rawdata)
    return parseddata

FREQUENCY={'d':'histoday', 'h':'histohour', 'm':'histominute'}

def get_historical_price(fromSymbol, toSymbol=_CURR, frequency='d', limit=2000):
    '''
    :param frequency: 'd', 'h' or 'm'
    :param limit: number of bars to return. I think max is 2000
    :return: get the last bars of fromSymbol in unit of fromSymbol
    '''
    url = f"{_URL_CRYPTOCOMPARE}/{FREQUENCY[frequency]}?fsym={fromSymbol}&tsym={toSymbol}&limit={limit}"  #&e={exchange}"
    rawdata = _requests.get(url).content.decode()
    parseddata = _loads(rawdata)
    try:
        df = _DataFrame(parseddata['Data'])
        if not df.empty:
            df = df.set_index('time')
            df.index = _to_datetime(df.index, unit='s')
    except Exception as inst:
        print(f"{type(inst)}: {inst}")    # the exception instance
        df = _DataFrame()
    return df


if __name__=='__main__':
    meta = get_meta()

    data1 = get_historical_price('ETH',limit=100, frequency='m')
    kraken_coin = get_kraken_coin() #['BTC','XRP','ETH','BCH','LTC','XMR','DASH','ZEC','ETC','REP']
