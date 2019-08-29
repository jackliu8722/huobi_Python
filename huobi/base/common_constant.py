class CommonConstant:
    UTF8 = "UTF-8"

    LOCAL_ADDRESS = "localhost"

    CODEC_PROTOBUF = "protobuf"

    # http方法
    METHOD_GET = "GET"

    METHOD_POST = "POST"

    SCHEME_HTTP = "http"

    SCHEME_HTTPS = "https"

    # 分隔符

    SEPARATOR_SEMICOLON = ";"

    SEPARATOR_QUESTION_MARK = "?"

    SEPARATOR_COLON = ":"

    SEPARATOR_COLON2 = "::"

    SEPARATOR_COMMA = ","

    SEPARATOR_AMPERSAND = "&"

    SEPARATOR_EQUAL_SIGN = "="

    SEPARATOR_VIRGULE = "/"

    SEPARATOR_BLANK = ""

    SEPARATOR_ASTERISK = "*"

    JSON_TYPE = "application/json;charset=UTF-8"

    # 交易所编码参数名称
    EXCHANGE_CODE = "exchangeCode"

    # 数据编码名称
    CODEC = "X-HB-Codec"

    # 交易所pro的id
    EXCHANGE_PRO_ID = 1

    # 交易所pro的code
    EXCHANGE_PRO_CODE = "pro"

    # 交易所hadax的id
    EXCHANGE_HADAX_ID = 2

    # 交易所hadax的code
    EXCHANGE_HADAX_CODE = "hadax"

    # huobi10指数
    SYMBOLS_TYPE_INDEX_HUOBI10 = "huobi10"

    # hb10基金净值
    SYMBOLS_TYPE_INDEX_HB10 = "hb10"

    # 无效exId
    INVALID_EXCHANGE_ID = 0

    # 无效instId
    INVALID_INST_ID = 0

    # Datadogmentric
    # session存活数量
    STAT_WS_LIVE = "client.ws.live"

    # req请求数量
    STAT_WS_REQ = "client.ws.req"

    # req请求时间
    STAT_REQ_EB_TS = "client.req.eb.ts"

    # req请求时间
    STAT_REQ_HANDLE_TS = "client.req.handle.ts"

    STAT_WS_CLOSE = "client.ws.close"

    # gateway向client推送消息量
    STAT_WS_SUB_PUSH = "client.sub.send"

    # rest kline
    STAT_REST_KLINE = "rest.kline"

    # req请求阈值
    STAT_REQ_THRESHOLD = 20

    # rest请求阈值
    STAT_REST_THRESHOLD = 50

    # 系统最小时间
    SYSTEM_TIME = 1325347200

    # 单次查询K线的最大数量
    CANDLESTICK_LIMIT = 1500

    # 深度p10类型限制大小
    DEPTH_P10_LIMIT = 200

    # 数据库查询最小间隔
    DB_QUERY_MIN_INTERVAL = 120000

    # 交易对分片数量
    SYMBOL_SHARDING = 16

    # 客户端连接分片数量
    CLIENT_SHARDING = 8

    # 深度数据增量推送频率
    DEPTH_DELTA_NUM = 5
