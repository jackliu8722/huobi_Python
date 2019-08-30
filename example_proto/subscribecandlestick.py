import sys
import logging
from huobi import SubscribeProtoClient
from huobi.model_proto import *
from huobi.base.app_constant import *
from huobi.exception.huobiapiexception import HuobiApiException

logger = logging.getLogger("huobi-client")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)



def callback(candlestick_event: 'CandlestickEvent'):
    print("Symbol: " + candlestick_event.symbol)
    print("Time: " + str(candlestick_event.data.timestamp))
    print("High: " + str(candlestick_event.data.high))
    print("Low: " + str(candlestick_event.data.low))
    print("Open: " + str(candlestick_event.data.open))
    print("Close: " + str(candlestick_event.data.close))
    print("Trades Volume: " + str(candlestick_event.data.volume))
    print("Trades Amount: " + str(candlestick_event.data.amount))
    print("Trades Nums: " + str(candlestick_event.data.count))
    print()


def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)

subscribe_client = SubscribeProtoClient()
try:
    subscribe_client.subscribe_candlestick_event("btcusdt,ethusdt,eosusdt", CandlestickInterval.MIN_15, callback, error)
except Exception as e:
    print(e)
