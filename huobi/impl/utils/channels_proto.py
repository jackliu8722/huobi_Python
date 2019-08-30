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


    def trade_channel(symbol):
        channel = dict()
        channel["sub"] = "market." + symbol + ".trade.detail"
        channel["id"] = str(get_current_timestamp())
        return json.dumps(channel)

    @staticmethod
    def price_depth_channel(symbol, levels, step):
        channel = dict()
        channel["ch"] = "mbp#" + symbol + "@" + (str(levels)) + "." + step
        channel["action"] = "sub"
        return json.dumps(channel)


    def orders_channel(symbol):
        channel = dict()
        channel["op"] = "sub"
        channel["cid"] = str(get_current_timestamp())
        channel["topic"] = "orders." + symbol
        return json.dumps(channel)


    def trade_statistics_channel(symbol):
        channel = dict()
        channel["sub"] = "market." + symbol + ".detail"
        channel["id"] = str(get_current_timestamp())
        return json.dumps(channel)


    def account_channel(mode):
        channel = dict()
        channel["op"] = "sub"
        channel["cid"] = str(get_current_timestamp())
        channel["topic"] = "accounts"
        channel["mode"] = mode
        return json.dumps(channel)
