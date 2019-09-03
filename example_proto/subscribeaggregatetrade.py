import logging
from huobi import SubscribeProtoClient
from huobi.base.app_constant import TradeDirectionValue
from huobi.model_proto import *

logger = logging.getLogger("huobi-client")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

sub_client = SubscribeProtoClient()


def callback(aggr_trade_event: 'AggregateTradeEvent'):
    print("Timestamp: " + str(aggr_trade_event.timestamp))
    print("Symbol: " + aggr_trade_event.symbol)
    print("Time: " + str(aggr_trade_event.data.timestamp))
    print("First Trade Id: " + str(aggr_trade_event.data.first_trade_id))
    print("Last Trade Id: " + str(aggr_trade_event.data.last_trade_id))
    print("Price: " + str(aggr_trade_event.data.price))
    print("Trades Volume: " + str(aggr_trade_event.data.volume))
    trade_side_desc = "buy" if TradeDirectionValue.BUY == aggr_trade_event.data.side else "sell"
    print("Trades side: " + trade_side_desc)
    print()


def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)


sub_client.subscribe_aggregate_trade_event("btcusdt,ethusdt,eosusdt", callback, error)
