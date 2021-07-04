# -*- coding: utf-8 -*-
# Create your tests here.
import json
from bitbank_client.sync import Client
import FinanceDataReader as fdr
from datetime import date, timedelta
import pyupbit
import ccxt
import pybithumb


def CurrencyConverter(value, old='KRW', new='USD'):
    # print(today)
    for i in range (999):
        currentDate = date.today() - timedelta(i)
        currentDate_str = currentDate.strftime("%Y-%m-%d")
        df = fdr.DataReader(old+'/'+new, currentDate_str)

        if df.empty: #현재 환율 정보가 없으면 어제 환율로 계산
            continue
        else:
            return df.Close[0] * value

#업비트 판매가 불러오기
def getUpbitSellPrice():
    price = pyupbit.get_current_price("KRW-XRP")
    return price

#비트뱅크 판매가 불러오기
def getBitbankSellPrice(jpy_option = False):
    client = Client(public_key='25667342-84a7-44ed-8c3c-55db676da962', private_key='08205db2036d5a550aa946687b89f4f189686a0cbe1005877a63c6129ee17f3c')
    response = client.get_ticker(pair='xrp_jpy')
    # print(response.status_code, response.json())
    JPYBuyPrice = float(response.json()["data"]["buy"])
    
    if jpy_option == False: 
        return CurrencyConverter(JPYBuyPrice, 'JPY', 'KRW') # 원화로 반환
    else:
        return JPYBuyPrice # 엔화로 반환

#바이낸스 판매가 불러오기
def getBinanceSellPrice():
    binance = ccxt.binance()
    ticker = binance.fetch_ticker('XRP/USDT')
    return CurrencyConverter(ticker['close'], 'USD', 'KRW') # 달러를 원화로 변환
    # print(ticker['open'], ticker['high'], ticker['low'], ticker['close'])

#빗썸 판매가 불러오기
def getBithumbSellPrice():
    price = pybithumb.get_current_price("XRP")
    return price

def getKimpRate(index = 0):
    rateList = []

    if index == 0 or index == 2:
        upbitSell = getUpbitSellPrice()
    if index == 1 or index == 3:
        bithumbSell = getBithumbSellPrice()
    if index == 0 or index == 1:
        bitBankSell = getBitbankSellPrice()
    if index == 2 or index == 3:
        binanceSell = getBinanceSellPrice()

    if index == 0:
        kimpRate_bitbank_to_upbit = (upbitSell-bitBankSell) / bitBankSell * 100
        return kimpRate_bitbank_to_upbit
    if index == 1:
        kimpRate_bitbank_to_bithumb = (bithumbSell-bitBankSell) / bitBankSell * 100
        return kimpRate_bitbank_to_bithumb
    if index == 2:
        kimpRate_binance_to_upbit = (upbitSell-binanceSell) / binanceSell * 100
        return kimpRate_binance_to_upbit
    if index == 3:
        kimpRate_binance_to_bithumb = (bithumbSell-binanceSell) / binanceSell * 100
        return kimpRate_binance_to_bithumb


# print("환율 : ", CurrencyConverter(0.6668, 'USD', 'KRW'))
# print("비트뱅크 리플 구매가격(원) : ", getBitbankSellPrice(), "원")
# print("업비트 리플 구매가격(원)", getUpbitSellPrice(), "원")
# print("바이낸스 리플 구매가격(원)", getBinanceSellPrice(), "원")
# print("빗썸 리플 구매가격(원)", getBithumbSellPrice(), "원")
# print("김프 : ", getKimpRate(), "%")

