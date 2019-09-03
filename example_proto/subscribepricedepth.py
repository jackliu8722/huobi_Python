import logging

from huobi import SubscribeProtoClient
from huobi.impl.utils.channels_proto import ChannelsProto
from huobi.model_proto import *

logger = logging.getLogger("huobi-client")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

sub_client = SubscribeProtoClient()


def callback(price_depth_event: 'PriceDepthEvent'):
    print("Timestamp: " + str(price_depth_event.timestamp))
    depth = price_depth_event.data
    if depth.delta:
        print("Only Increased Data!")
    else:
        print("It's All Data!")

    for entry in depth.bids:
        print("Bids: " + " price: " + str(entry.price) + ", size: " + str(entry.size))

    for entry in depth.asks:
        print("Asks: " + " price: " + str(entry.price) + ", size: " + str(entry.size))


def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)


sub_client.subscribe_price_depth_event("btcusdt,ethusdt,eosusdt", 10, "s0", callback, error)
#sub_client.subscribe_price_depth_event("btcusdt", 10, None, callback, error)
#sub_client.subscribe_price_depth_event("btcusdt", 3, "s0", callback, error)
#sub_client.subscribe_price_depth_event("btcusdt", None, None, callback, error)

