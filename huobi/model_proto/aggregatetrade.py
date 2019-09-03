class AggregateTrade:
    """
    The trade received by subscription of trade.

    :member
        symbol: The symbol you subscribed.
        timestamp: The UNIX formatted timestamp generated by server in UTC.
        trade_list: The trade list. The content is Trade class.
    """

    def __init__(self):
        self.timestamp = 0
        self.first_trade_id = 0
        self.last_trade_id = 0
        self.price = 0.0
        self.volume = 0.0
        self.side = 0.0
