class WSRequest:
    def __init__(self):
        self.subscription_handler = None
        self.is_trading = False
        self.error_handler = None
        self.parser = None
        self.update_callback = None
