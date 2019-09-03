import time
import sys
import json

from huobi.base.app_constant import PriceDepthSetting
from huobi.impl.webprotorequest import WebProtoRequest
from huobi.impl.utils.channels_proto import ChannelsProto
from huobi.impl.utils.channelparser import ChannelParser
from huobi.impl.accountinfomap import account_info_map
from huobi.impl.utils.timeservice import *
from huobi.impl.utils.inputchecker import *
from huobi.model_proto import *
from huobi.model_proto.aggregatetrade import AggregateTrade
from huobi.model_proto.aggregatetradeevent import AggregateTradeEvent
from huobi.model_proto.detailtrade import DetailTrade
from huobi.model_proto.detailtradeevent import DetailTradeEvent
from huobi.model_proto.overview import Overview
from huobi.model_proto.overviewevent import OverviewEvent
from huobi.model_proto.overviewtick import OverviewTick


class WebProtoRequestImpl(object):

    def __init__(self, api_key):
        self.__api_key = api_key

    def subscribe_candlestick_event(self, symbols, interval, callback, error_handler=None):
        check_symbol_list(symbols)
        check_should_not_none(interval, "interval")
        check_should_not_none(callback, "callback")

        def subscription_handler(connection):
            for val in symbols:
                connection.send(ChannelsProto.candlestick_channel(val, interval))
                time.sleep(0.01)

        def parse(r):
            candlestick_event = CandlestickEvent()
            item = r.data

            candlestick_event.symbol = item.symbol
            candlestick_event.interval = interval
            candlestick_event.timestamp = convert_cst_in_millisecond_to_utc(item.ts)
            data = Candlestick()
            data.timestamp = convert_cst_in_second_to_utc(item.id)
            data.open = item.open
            data.close = item.close
            data.low = item.low
            data.high = item.high
            data.amount = item.turnover
            data.count = item.num_of_trades
            data.volume = item.volume
            candlestick_event.data = data

            return candlestick_event

        request = WebProtoRequest()
        request.subscription_handler = subscription_handler
        request.is_trading = False
        request.parser = parse
        request.update_callback = callback
        request.error_handler = error_handler
        return request

    def subscribe_24h_trade_statistics_event(self, symbols, callback, error_handler=None):
        check_symbol_list(symbols)
        check_should_not_none(callback, "callback")

        def subscription_handler(connection):
            for symbol in symbols:
                connection.send(ChannelsProto.trade_statistics_channel(symbol))
                time.sleep(0.01)

        def parse(r):
            event_obj = TradeStatisticsEvent()
            item = r.data
            event_obj.symbol = item.symbol
            event_obj.timestamp = convert_cst_in_millisecond_to_utc(item.ts)
            data = TradeStatistics()
            data.timestamp = convert_cst_in_second_to_utc(item.ts)
            data.symbol = item.symbol
            data.open = item.open
            data.close = item.close
            data.low = item.low
            data.high = item.high
            data.amount = item.turnover
            data.count = item.num_of_trades
            data.volume = item.volume
            event_obj.trade_statistics = data

            return event_obj

        request = WebProtoRequest()
        request.subscription_handler = subscription_handler
        request.is_trading = False
        request.parser = parse
        request.update_callback = callback
        request.error_handler = error_handler
        return request

    def subscribe_aggregate_trade_event(self, symbols, callback, error_handler=None):
        check_symbol_list(symbols)
        check_should_not_none(callback, "callback")

        def subscription_handler(connection):
            for symbol in symbols:
                connection.send(ChannelsProto.aggregate_trade_channel(symbol))
                time.sleep(0.01)

        def parse(r):
            event_obj = AggregateTradeEvent()
            item = r.data
            event_obj.symbol = item.symbol
            event_obj.timestamp = convert_cst_in_millisecond_to_utc(item.ts)
            data = AggregateTrade()
            data.timestamp = convert_cst_in_second_to_utc(item.ts)
            data.symbol = item.symbol
            data.first_trade_id = item.first_trade_id
            data.last_trade_id = item.last_trade_id
            data.price = item.price
            data.volume = item.volume
            data.side = item.side
            event_obj.data = data

            return event_obj

        request = WebProtoRequest()
        request.subscription_handler = subscription_handler
        request.is_trading = False
        request.parser = parse
        request.update_callback = callback
        request.error_handler = error_handler
        return request

    def subscribe_detail_trade_event(self, symbols, callback, error_handler=None):
        check_symbol_list(symbols)
        check_should_not_none(callback, "callback")

        def subscription_handler(connection):
            for symbol in symbols:
                connection.send(ChannelsProto.detail_trade_channel(symbol))
                time.sleep(0.01)

        def parse(r):
            event_obj = DetailTradeEvent()
            item = r.data
            event_obj.symbol = item.symbol
            event_obj.timestamp = convert_cst_in_millisecond_to_utc(item.ts)
            data = DetailTrade()
            data.timestamp = convert_cst_in_second_to_utc(item.ts)
            data.symbol = item.symbol
            data.trade_id = item.trade_id
            data.price = item.price
            data.volume = item.volume
            data.side = item.side
            event_obj.data = data

            return event_obj

        request = WebProtoRequest()
        request.subscription_handler = subscription_handler
        request.is_trading = False
        request.parser = parse
        request.update_callback = callback
        request.error_handler = error_handler
        return request

    def subscribe_overview_event(self, callback, error_handler=None):
        check_should_not_none(callback, "callback")

        def subscription_handler(connection):
            connection.send(ChannelsProto.overview_channel())

        def format_tick_entry(tickObj):
            overview_tick = OverviewTick()
            overview_tick.symbol = tickObj.symbol
            overview_tick.open = tickObj.open
            overview_tick.close = tickObj.close
            overview_tick.low = tickObj.low
            overview_tick.high = tickObj.high
            overview_tick.amount = tickObj.turnover
            overview_tick.count = tickObj.num_of_trades
            overview_tick.volume = tickObj.volume
            return overview_tick

        def parse(r):
            event_obj = OverviewEvent()
            item = r.data

            event_obj.timestamp = convert_cst_in_millisecond_to_utc(item.ts)
            data = Overview()

            data.timestamp = convert_cst_in_second_to_utc(item.ts)
            if len(item.ticks):
                for row in item.ticks:
                    data.ticks.append(format_tick_entry(row))

            event_obj.data = data

            return event_obj

        request = WebProtoRequest()
        request.subscription_handler = subscription_handler
        request.is_trading = False
        request.parser = parse
        request.update_callback = callback
        request.error_handler = error_handler
        return request

    def subscribe_price_depth_event(self, symbols, levels, step, callback, error_handler=None):
        check_symbol_list(symbols)
        check_should_not_none(callback, "callback")

        def subscription_handler(connection):
            for val in symbols:
                connection.send(ChannelsProto.price_depth_channel(symbol=val, levels=levels, step=step))
                time.sleep(0.01)

        def format_depth_entry(price, size):
            depth_entry = DepthEntry()
            depth_entry.price = price
            depth_entry.size = size
            return depth_entry

        def parse(r):
            event_obj = PriceDepthEvent()
            item = r.data

            event_obj.symbol = item.symbol
            event_obj.timestamp = get_current_timestamp()
            data = PriceDepth()

            if len(item.bids):
                for row in item.bids:
                    data.bids.append(format_depth_entry(price=row.price, size=row.size))
            if len(item.asks):
                for row in item.asks:
                    data.asks.append(format_depth_entry(price=row.price, size=row.size))

            data.delta = item.delta
            event_obj.data = data

            return event_obj

        request = WebProtoRequest()
        request.subscription_handler = subscription_handler
        request.is_trading = False
        request.parser = parse
        request.update_callback = callback
        request.error_handler = error_handler
        return request

    # def subscribe_order_update(self, symbols, callback, error_handler=None):
    #     check_symbol_list(symbols)
    #     check_should_not_none(callback, "callback")
    #
    #     def subscription_handler(connection):
    #         for val in symbols:
    #             connection.send(orders_channel(val))
    #             time.sleep(0.01)
    #
    #     def parse(json_wrapper):
    #         ch = json_wrapper.get_string("topic")
    #         parse = ChannelParser(ch)
    #         order_update_event = OrderUpdateEvent()
    #         order_update_event.symbol = parse.symbol
    #         order_update_event.timestamp = convert_cst_in_millisecond_to_utc(json_wrapper.get_int("ts"))
    #         data = json_wrapper.get_object("data")
    #         order = Order()
    #         order.order_id = data.get_int("order-id")
    #         order.symbol = parse.symbol
    #         order.account_type = account_info_map.get_account_by_id(self.__api_key,
    #                                                                 data.get_int("account-id")).account_type
    #         order.amount = data.get_float("order-amount")
    #         order.price = data.get_float("order-price")
    #         order.created_timestamp = convert_cst_in_millisecond_to_utc(data.get_int("created-at"))
    #         order.order_type = data.get_string("order-type")
    #         order.filled_amount = data.get_float("filled-amount")
    #         order.filled_cash_amount = data.get_float("filled-cash-amount")
    #         order.filled_fees = data.get_float("filled-fees")
    #         order.state = data.get_string("order-state")
    #         order.source = data.get_string("order-source")
    #         order_update_event.data = order
    #         return order_update_event
    #
    #     request = WebsocketRequest()
    #     request.subscription_handler = subscription_handler
    #     request.is_trading = True
    #     request.parser = parse
    #     request.update_callback = callback
    #     request.error_handler = error_handler
    #     return request
    #
    # def subscribe_account_event(self, mode, callback, error_handler=None):
    #     check_should_not_none(mode, "mode")
    #     check_should_not_none(callback, "callback")
    #
    #     def subscription_handler(connection):
    #         connection.send(account_channel(mode))
    #
    #     def parse(json_wrapper):
    #         account_event = AccountEvent()
    #         account_event.timestamp = convert_cst_in_millisecond_to_utc(json_wrapper.get_int("ts"))
    #         data = json_wrapper.get_object("data")
    #         account_event.change_type = data.get_string("event")
    #         list_array = data.get_array("list")
    #         account_change_list = list()
    #         for item in list_array.get_items():
    #             account_change = AccountChange()
    #             account_change.account_type = account_info_map.get_account_by_id(self.__api_key, item.get_int(
    #                 "account-id")).account_type
    #             account_change.currency = item.get_string("currency")
    #             account_change.balance = item.get_float("balance")
    #             account_change.balance_type = item.get_string("type")
    #             account_change_list.append(account_change)
    #         account_event.account_change_list = account_change_list
    #         return account_event
    #
    #     request = WebsocketRequest()
    #     request.subscription_handler = subscription_handler
    #     request.is_trading = True
    #     request.parser = parse
    #     request.update_callback = callback
    #     request.error_handler = error_handler
    #     return request
