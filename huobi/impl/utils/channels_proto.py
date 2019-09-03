import json

from huobi.base.app_constant import PriceDepthSetting
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



    @staticmethod
    def price_depth_channel(symbol, levels = None, step = None):
        print ("price_depth_channel params : " + symbol + "\t" + (str(levels)) + "\t" + (str(step)))
        channel = dict()
        if levels and (levels in PriceDepthSetting.LEVELS):
            if step and (step in PriceDepthSetting.STEP):
                channel["ch"] = "mbp#" + symbol + "@" + (str(levels)) + "." + step
            else:
                channel["ch"] = "mbp#" + symbol + "@" + (str(levels))
        else:
            channel["ch"] = "mbp#btcusdt@p10"

        channel["action"] = "sub"
        print ("depth channel : " + channel["ch"])
        return json.dumps(channel)



    @staticmethod
    def trade_statistics_channel(symbol):
        channel = dict()
        channel["ch"] = "summary#" + symbol
        channel["action"] = "sub"
        return json.dumps(channel)

    @staticmethod
    def aggregate_trade_channel(symbol):
        channel = dict()
        channel["ch"] = "aggrTrades#" + symbol
        channel["action"] = "sub"
        return json.dumps(channel)

    @staticmethod
    def detail_trade_channel(symbol):
        channel = dict()
        channel["ch"] = "trades#" + symbol
        channel["action"] = "sub"
        return json.dumps(channel)

    @staticmethod
    def overview_channel():
        channel = dict()
        channel["ch"] = "overview"
        channel["action"] = "sub"
        return json.dumps(channel)
