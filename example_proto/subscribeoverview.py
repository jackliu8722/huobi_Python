import logging
from huobi import SubscribeProtoClient
from huobi.model_proto import *

logger = logging.getLogger("huobi-client")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

sub_client = SubscribeProtoClient()


def callback(overview_event: 'OverviewEvent'):
    timestamp_cur = str(overview_event.timestamp)
    print("Timestamp: " + timestamp_cur)
    overview = overview_event.data

    print (timestamp_cur + " row counts : " + str(len(overview.ticks)))
    for idx, tick in enumerate(overview.ticks):
        print("\tTisks " + str(idx) + " info: " )
        print("\tSymbol: " + str(tick.symbol))
        print("\tAmount: " + str(tick.amount))
        print("\tVolume: " + str(tick.volume))
        print("\tNums: " + str(tick.count))
        print("\tOpen: " + str(tick.open))
        print("\tClose: " + str(tick.close))
        print("\tHigh: " + str(tick.high))
        print("\tLow: " + str(tick.low))
        print()
    print()


def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)


sub_client.subscribe_overview_event(callback, error)
