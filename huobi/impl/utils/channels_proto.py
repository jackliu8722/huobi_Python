import json
from huobi.impl.utils.timeservice import get_current_timestamp

class ChannelsProto:
    def __init__(self):
        pass

    @staticmethod
    def candlestick_channel(symbol, interval):
        channel = dict()
        channel["ch"] = "candlestick#" + symbol + "@" + interval
        channel["action"] = "sub"
        return json.dumps(channel)


