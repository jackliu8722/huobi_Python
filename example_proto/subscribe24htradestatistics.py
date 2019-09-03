import logging
from huobi import SubscribeProtoClient
from huobi.model_proto import *

logger = logging.getLogger("huobi-client")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)




def callback(trade_statistics_event: 'TradeStatisticsEvent'):
    print("Timestamp: " + str(trade_statistics_event.timestamp))
    print("Symbol: " + str(trade_statistics_event.symbol))
    print("Timestamp: " + str(trade_statistics_event.trade_statistics.timestamp))
    print("High: " + str(trade_statistics_event.trade_statistics.high))
    print("Low: " + str(trade_statistics_event.trade_statistics.low))
    print("Open: " + str(trade_statistics_event.trade_statistics.open))
    print("Close: " + str(trade_statistics_event.trade_statistics.close))
    print("Trades Volume: " + str(trade_statistics_event.trade_statistics.volume))
    print("Trades Amount: " + str(trade_statistics_event.trade_statistics.amount))
    print("Trades Nums: " + str(trade_statistics_event.trade_statistics.count))
    """
    print("Trades symbol: " + str(trade_statistics_event.symbol))
    print("Trades timestamp: " + str(trade_statistics_event.timestamp))
    print('class TradeStatisticsEvent:', ', '.join(['%s:%s' % item for item in trade_statistics_event.trade_statistics.__dict__.items()]))
    print("Trades Volume: " + str(trade_statistics_event.trade_statistics.volume))
    print("Trades Amount: " + str(trade_statistics_event.trade_statistics.amount))
    """


try:
    sub_client = SubscribeProtoClient()
    sub_client.subscribe_24h_trade_statistics_event("btcusdt,ethusdt,eosusdt", callback)
except Exception as e:
    print(e)
