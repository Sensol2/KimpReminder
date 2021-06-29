# Create your tests here.
from sync import Client
import json
from currency_converter import CurrencyConverter

#비트뱅크 판매가 불러오기
client = Client(public_key='25667342-84a7-44ed-8c3c-55db676da962', private_key='08205db2036d5a550aa946687b89f4f189686a0cbe1005877a63c6129ee17f3c')
response = client.get_ticker(pair='xrp_jpy')
# print(response.status_code, response.json())
JPYBuyPrice = float(response.json()["data"]["buy"])
print("구매가격 : ", JPYBuyPrice)

# 환율변환
c = CurrencyConverter()
KRWBuyPrice = float(c.convert(JPYBuyPrice,'JPY','KRW'))
print(KRWBuyPrice, "원")

#
# async
#


# from async_ import Async

# import grequests

# client = Async(public_key='25667342-84a7-44ed-8c3c-55db676da962', private_key='08205db2036d5a550aa946687b89f4f189686a0cbe1005877a63c6129ee17f3c')
# reqs = [client.get_ticker(pair='xrp_jpy'), client.get_depth(pair='xrp_jpy'), ...]
# response = grequests.map(reqs)
# for r in response:
# 	print(r.status_code, r.json())


# print(client.get_ticker(pair='btc_jpy'))# GET /{pair}/ticker
# client.get_depth(pair='btc_jpy') # GET /{pair}/depth
# client.get_transactions(pair='btc_jpy') # GET /{pair}/transactions
# client.get_transactions(pair='btc_jpy', yyyymmdd='20180509') # GET /{pair}/transactions/{YYYYMMDD}
# client.get_candlestick(pair='btc_jpy', candle_type='1day', yyyymmdd='2018') # GET /{pair}/candlestick/{candle-type}/{YYYY}
# client.get_candlestick(pair='btc_jpy', candle_type='1hour', yyyymmdd='20180510') # GET /{pair}/candlestick/{candle-type}/{YYYY}
# client.get_assets() # GET /user/assets
# client.get_order(pair='btc_jpy', order_id=1) # GET /user/spot/order
# client.order(pair='btc_jpy', amount=1, price=1, side='buy', type='limit') # POST /user/spot/order
# client.cancel_order(pair='btc_jpy', order_id=1) # POST /user/spot/cancel_order
# client.cancel_orders(pair='btc_jpy', order_ids=[1,2]) # POST /user/spot/cancel_orders
# client.orders_info(pair='btc_jpy', order_ids=[1,2]) # POST /user/spot/orders_info
# client.get_active_orders(pair='btc_jpy') # GET /user/spot/active_orders
# client.get_trade_history(pair='btc_jpy') # GET /user/spot/trade_history
# client.get_withdrawal_account(asset='btc') # GET /user/withdrawal_account
# client.request_withdrawal(asset='btc', uuid=1, amount=1) # POST /user/request_withdrawal
# client.request_withdrawal(asset='btc', uuid=1, amount=1, otp_token='xxx') # POST /user/request_withdrawal
# client.request_withdrawal(asset='btc', uuid=1, amount=1, sms_token='xxx') # POST /user/request_withdrawal
