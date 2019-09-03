import sys
from huobi.protodecode.market_downstream_protocol_pb2 import Action
from . import market_downstream_protocol_pb2


class EventDecoder:
    def __init__(self):
        pass

    @staticmethod
    def decode(data):
        if not data:
            return None

        r = EventDecoder.R()
        try:
            result = market_downstream_protocol_pb2.Result().FromString(data)
            #print ("decode on message receive data === : " + (str(data)))
            #print ("decode Sequence === : " + (str(result.sequence)))
            #print ("decode Code === : " + (str(result.code)))

            r.seq = None if not result.sequence else result.sequence
            r.code = None if not result.code else result.code
            r.message = None if not result.message else result.message
            r.action = result.action
            r.ch = result.ch
            if result.data.value:
                r.data = EventDecoder.decodeData(result)

            #print ("decode Sequence : " + (str(r.seq)))
            #print ("decode Code : " + (str(r.code)))
            return r
        except Exception as ex:
            print ("<<<<<<<<<<<<<< " + ("%s " % (sys._getframe().f_code.co_name)) + " >>>>>>>>>>>>>   exception catched")
            print(ex)
            return r

        return r

    @staticmethod
    def decodeData(result):
        try:
            if not result.data:
                return None

            print ("<<<<<<<<<<<<<< " + ("%s " % (sys._getframe().f_code.co_name)) + " >>>>>>>>>>>>>   action  : " + (str(result.action)) + ",  channel :"+ result.ch)
            if (result.action == Action.PING):
                return EventDecoder.decodePing(result)

            ch = result.ch
            if (ch.startswith("candlestick")):
                if (result.action == Action.PUSH):
                    return EventDecoder.decodeCandlestick(result)
                else:
                    return EventDecoder.decodeReqCandlestick(result)

            if (ch.startswith("mbp")):
                return EventDecoder.decodeMbp(result)

            if (ch.startswith("overview")):
                return EventDecoder.decodeOverview(result)

            if (ch.startswith("summary")):
                return EventDecoder.decodeSummary(result)

            if (ch.startswith("aggrTrade")):
                return EventDecoder.decodeAggrTrade(result)

            if (ch.startswith("trades")):
                if (result.action == Action.PUSH):
                    return EventDecoder.decodeTrade(result)
                else:
                    return EventDecoder.decodeReqTrade(result)

            print ("<<<<<<<<<<<<<< " + ("%s " % (sys._getframe().f_code.co_name)) + " >>>>>>>>>>>>>   action  : " + (str(result.action)) + ",  channel :" + result.ch + "   -- unprocessed")

            return None
        except Exception as ex:
            print ("<<<<<<<<<<<<<< " + ("%s " % (sys._getframe().f_code.co_name)) + " >>>>>>>>>>>>>   exception catched")
            print(ex)
            return None

    @staticmethod
    def decodePing(result):
        p = market_downstream_protocol_pb2.Ping()
        result.data.Unpack(p)
        ping = EventDecoder.Ping()
        ping.ts = p.ts

        return ping

    @staticmethod
    def decodeCandlestick(result):
        d = market_downstream_protocol_pb2.Candlestick()
        result.data.Unpack(d)

        e = EventDecoder.Candlestick()
        e.close = d.close
        e.high = d.high
        e.id = d.id
        e.symbol = d.symbol
        e.open = d.open
        e.low = d.low
        e.num_of_trades = d.num_of_trades
        e.turnover = d.turnover
        e.volume = d.volume
        e.ts = d.ts

        return e

    @staticmethod
    def decodeReqCandlestick(result):
        d = market_downstream_protocol_pb2.ReqCandlestick()
        result.data.Unpack(d)

        e = EventDecoder.ReqCandlestick()
        e.symbol = d.symbol
        e.candlesticks = d.candlesticks

        return e

    @staticmethod
    def decodeMbp(result):
        if ((result.action != Action.PUSH) and (result.action != Action.REQ)):
            return None

        d = market_downstream_protocol_pb2.Depth()
        result.data.Unpack(d)

        e = EventDecoder.Depth()
        e.symbol = d.symbol
        e.delta = d.delta
        e.bids = d.bids
        e.asks = d.asks

        return e

    @staticmethod
    def decodeReqTrade(result):
        d = market_downstream_protocol_pb2.ReqTrade()
        result.data.Unpack(d)

        e = EventDecoder.ReqTrade()
        e.symbol = d.symbol
        e.trades = d.trades

        return e

    @staticmethod
    def decodeTrade(result):
        d = market_downstream_protocol_pb2.Trade()
        result.data.Unpack(d)

        e = EventDecoder.Trades()
        e.symbol = d.symbol
        e.trade_id = d.trade_id
        e.ts = d.ts
        e.price = d.price
        e.volume = d.volume
        e.side = d.side

        return e


    @staticmethod
    def decodeOverview(result):
        if (result.action != Action.PUSH):
            return None

        d = market_downstream_protocol_pb2.Overview()
        result.data.Unpack(d)

        e = EventDecoder.Overview()
        e.ts = d.ts
        e.ticks = d.tick

        return e

    @staticmethod
    def decodeAggrTrade(result):
        if ((result.action != Action.PUSH) and (result.action != Action.REQ)):
            return None

        d = market_downstream_protocol_pb2.AggrTrade()
        result.data.Unpack(d)

        e = EventDecoder.AggrTrades()
        e.symbol = d.symbol
        e.first_trade_id = d.first_trade_id
        e.last_trade_id = d.last_trade_id
        e.ts = d.ts
        e.price = d.price
        e.volume = d.volume
        e.side = d.side

        return e

    @staticmethod
    def decodeSummary(result):
        if ((result.action != Action.PUSH) and (result.action != Action.REQ)):
            return None

        d = market_downstream_protocol_pb2.MarketSummary()
        result.data.Unpack(d)

        e = EventDecoder.Summary()
        e.close = d.close
        e.high = d.high
        e.id = d.id
        e.symbol = d.symbol
        e.low = d.low
        e.num_of_trades = d.num_of_trades
        e.turnover = d.turnover
        e.volume = d.volume
        e.open = d.open
        e.ts = d.ts

        return e


    class Ping:
        def __init__(self):
            self.ts = ""

    class Candlestick:
        def __init__(self):
            self.id = ""
            self.symbol = ""
            self.ts = ""
            self.open = ""
            self.close = ""
            self.low = ""
            self.high = ""
            self.num_of_trades = ""
            self.volume = ""
            self.turnover = ""

    class ReqCandlestick:
        def __init__(self):
            self.symbol = ""
            self.candlesticks = list()

        class Tick:
            def __init__(self):
                self.id = ""
                self.ts = ""
                self.open = ""
                self.close = ""
                self.low = ""
                self.high = ""
                self.num_of_trades = ""
                self.volume = ""
                self.turnover = ""

    class Depth:
        def __init__(self):
            self.ts = ""
            self.symbol = ""
            self.delta = ""
            self.bids = list()
            self.asks = list()

    class DepthTick:
        def __init__(self):
            self.price = ""
            self.size = ""

    class Overview:
        def __init__(self):
            self.ts = ""
            self.tick = list()   # tick 和原协议保持一致

    class OverviewTick:
        def __init__(self):
            self.symbol = ""
            self.open = ""
            self.close = ""
            self.low = ""
            self.high = ""
            self.num_of_trades = ""
            self.volume = ""
            self.turnover = ""

    class Summary:
        def __init__(self):
            self.id = ""
            self.symbol = ""
            self.ts = ""
            self.open = ""
            self.close = ""
            self.low = ""
            self.high = ""
            self.num_of_trades = ""
            self.volume = ""
            self.turnover = ""

    class ReqTrade:
        def __init__(self):
            self.symbol = ""
            self.trades = list()

        class Tick:
            def __init__(self):
                self.trade_id = ""
                self.ts = ""
                self.price = ""
                self.volume = ""
                self.side = ""

    class Trades:
        def __init__(self):
            self.symbol = ""
            self.trade_id = ""
            self.ts = ""
            self.price = ""
            self.volume = ""
            self.side = ""

    class AggrTrades:
        def __init__(self):
            self.symbol = ""
            self.first_trade_id = ""
            self.last_trade_id = ""
            self.ts = ""
            self.price = ""
            self.volume = ""
            self.side = ""

    class R:
        def __init__(self):
            self.action = ""
            self.ch = ""
            self.data = ""
            self.seq = ""
            self.code = ""
            self.message = ""
