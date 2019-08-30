import sys
import threading
import websocket
import ssl
import logging
from urllib import parse
import urllib.parse

from huobi.protodecode.event_decoder import EventDecoder
from huobi.protodecode.market_downstream_protocol_pb2 import Action
from huobi.impl.utils.timeservice import get_current_timestamp
from huobi.impl.utils.urlparamsbuilder import UrlParamsBuilder
from huobi.impl.utils.apisignature import create_signature
from huobi.exception.huobiapiexception import HuobiApiException
from huobi.base import CommonConstant

# Key: ws, Value: connection
ws_connection_handler = dict()


def on_message(ws, message):
    ws_connection = ws_connection_handler[ws]
    ws_connection.on_message(message)
    return


def on_error(ws, error):
    ws_connection = ws_connection_handler[ws]
    ws_connection.on_failure(error)


def on_close(ws):
    ws_connection = ws_connection_handler[ws]
    ws_connection.on_close()


def on_open(ws):
    ws_connection = ws_connection_handler[ws]
    ws_connection.on_open(ws)


connection_id = 0


class ConnectionState:
    IDLE = 0
    CONNECTING = 1
    CONNECTED = 2
    CLOSING = 3
    CLOSED_ON_ERROR = 4
    CLOSING_ON_ERROR = 5


def ws_func(*args):
    connection_instance = args[0]

    connection_instance.ws = websocket.WebSocketApp(connection_instance.url,
                                                    header=[
                                                        CommonConstant.EXCHANGE_CODE + ":" + CommonConstant.EXCHANGE_PRO_CODE,
                                                        CommonConstant.CODEC + ":" + CommonConstant.CODEC_PROTOBUF],
                                                    on_message=on_message,
                                                    on_error=on_error,
                                                    on_close=on_close)
    global ws_connection_handler
    ws_connection_handler[connection_instance.ws] = connection_instance
    connection_instance.logger.info("[Sub][" + str(connection_instance.id) + "] Connecting...")
    connection_instance.delay_in_second = -1
    connection_instance.ws.on_open = on_open
    connection_instance.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    connection_instance.logger.info("[Sub][" + str(connection_instance.id) + "] Connection event loop down")
    if connection_instance.state == ConnectionState.CONNECTED:
        connection_instance.state = ConnectionState.IDLE


class WebProtoConnection:

    def __init__(self, api_key, secret_key, uri, watch_dog, request):
        # threading.Thread.__init__(self)
        self.__lock = threading.Lock()
        self.__thread = None
        # self.__market_url = "wss://api.huobi.pro/ws"
        # self.__trading_url = "wss://api.huobi.pro/ws/v1"

        self.scheme = "ws://"
        self.market_url = "/ws"
        self.trading_url = "/ws/v1"
        self.api_url = "/api/ws"
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.request = request
        self.__watch_dog = watch_dog
        self.delay_in_second = -1
        self.ws = None
        self.last_receive_time = 0
        self.logger = logging.getLogger("huobi-client")
        self.state = ConnectionState.IDLE
        global connection_id
        connection_id += 1
        self.id = connection_id
        host = urllib.parse.urlparse(uri).hostname
        # if host.find("api.") == 0:
        #     self.__market_url = "wss://" + host + "/ws"
        #     self.__trading_url = "wss://" + host + "/ws/v1"
        # else:
        #     self.__market_url = "wss://" + host + "/api/ws"
        #     self.__trading_url = "wss://" + host + "/ws/v1"
        # if request.is_trading:
        #     self.url = self.__trading_url
        # else:
        #     self.url = self.__market_url
        self.__market_url = self.scheme + host + self.market_url
        self.__trading_url = self.scheme + host + self.trading_url
        #self.url = "ws://huobi-gateway.test-12.huobiapps.com/ws"  # 线下测试环境，订阅的时候只推送一条消息
        self.url = "wss://api.huobi.pro/spot/v2/ws"

    def in_delay_connection(self):
        return self.delay_in_second != -1

    def re_connect_in_delay(self, delay_in_second):
        self.delay_in_second = delay_in_second
        self.logger.warning("[Sub][" + str(self.id) + "] Reconnecting after "
                            + str(self.delay_in_second) + " seconds later")

    def re_connect(self):
        if self.delay_in_second != 0:
            self.delay_in_second -= 1
            self.logger.warning("In delay connection: " + str(self.delay_in_second))
        else:
            self.connect()

    def connect(self):
        with self.__lock:
            if self.state == ConnectionState.CONNECTED:
                self.logger.info("[Sub][" + str(self.id) + "] Already connected")
            else:
                self.state = ConnectionState.CONNECTING
                self.__thread = threading.Thread(target=ws_func, args=[self])
                self.__thread.start()

    def send(self, data):
        # print(data)
        self.ws.send(data)

    def on_close(self):
        del ws_connection_handler[self.ws]
        self.ws = None
        if self.state == ConnectionState.CLOSING:
            self.state = ConnectionState.IDLE
            self.__watch_dog.on_connection_closed(self)
            self.logger.error("[Sub][" + str(self.id) + "] Closed")
        elif self.state == ConnectionState.CLOSING_ON_ERROR:
            self.state = ConnectionState.CLOSED_ON_ERROR
            self.logger.error("[Sub][" + str(self.id) + "] Closed with error")
        else:
            self.logger.error("[Sub][" + str(self.id) + "] Closed unexpected state")

    def on_open(self, ws):
        # print("### open ###")
        self.logger.info("[Sub][" + str(self.id) + "] Connected to server")
        self.ws = ws
        self.last_receive_time = get_current_timestamp()
        self.state = ConnectionState.CONNECTED
        self.__watch_dog.on_connection_created(self)
        if self.request.is_trading:
            try:
                builder = UrlParamsBuilder()
                create_signature(self.__api_key, self.__secret_key,
                                 "GET", self.url, builder)
                builder.put_url("op", "auth")
                self.send(builder.build_url_to_json())
            except Exception as e:
                self.on_error("Unexpected error when create the signature: " + str(e))
        else:
            if self.request.subscription_handler is not None:
                self.request.subscription_handler(self)
        return

    def on_error(self, error_message):
        if self.request.error_handler is not None:
            exception = HuobiApiException(HuobiApiException.SUBSCRIPTION_ERROR, error_message)
            self.request.error_handler(exception)
        self.logger.error("[Sub][" + str(self.id) + "] " + str(error_message))

    def on_failure(self, error):
        self.on_error("Unexpected error: " + str(error))
        self.close_on_error()

    def on_message(self, message):

        try:
            self.last_receive_time = get_current_timestamp()

            r = EventDecoder.decode(message)

            if r is not None:
                if (r.action == Action.PING):
                    self.__process_ping_on_market_line(r)
                elif ((r.action == Action.PUSH) or (r.action == Action.REQ)):
                    self.__on_receive(r)
        except Exception as e:
            self.on_error("Failed to parse server's response: " + str(e))

    def __on_receive(self, r):
        res = None
        try:
            if self.request.parser is not None and r is not None:
                res = self.request.parser(r)
        except Exception as e:
            self.on_error("Failed to parse receive message: " + str(e))

        try:
            if self.request.update_callback is not None:
                self.request.update_callback(res)
        except Exception as e:
            self.on_error("Process error: " + str(e)
                          + " You should capture the exception in your error handler")

    def __process_ping_on_trading_line(self):
        self.send("{\"op\":\"pong\",\"ts\":" + str(get_current_timestamp()) + "}")
        return

    def __process_ping_on_market_line(self, r):
        pingTime = r.data.ts
        self.send("{\"action\":\"pong\",\"ts\":" + str(pingTime) + "}")
        return

    def close(self):
        with self.__lock:
            if self.ws is not None:
                self.state = ConnectionState.CLOSING
                self.ws.close()
                self.logger.error("[Sub][" + str(self.id) + "] Closing normally")

    def close_on_error(self):
        with self.__lock:
            if self.ws is not None:
                self.state = ConnectionState.CLOSING_ON_ERROR
                self.ws.close()
                self.logger.error("[Sub][" + str(self.id) + "] Connection is closing due to error")
