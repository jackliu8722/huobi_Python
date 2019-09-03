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


def callback(detail_event: 'DetailTradeEvent'):
    print("Timestamp: " + str(detail_event.timestamp))
    print("Symbol: " + detail_event.symbol)
    print("Timestamp: " + str(detail_event.data.timestamp))
    print("Price: " + str(detail_event.data.price))
    print("Volume: " + str(detail_event.data.volume))
    trade_side_desc = "buy" if TradeDirectionValue.BUY == detail_event.data.side else "sell"
    print("Trades side: " + trade_side_desc)
    print()


def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)


sub_client.subscribe_detail_trade_event("btcusdt,ethusdt,eosusdt", callback, error)
