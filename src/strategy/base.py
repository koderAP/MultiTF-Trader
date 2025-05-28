class BaseStrategy:
    def __init__(self, data_15m, data_1h):
        self.data_15m = data_15m
        self.data_1h = data_1h

    def generate_signals(self):
        raise NotImplementedError("Must implement generate_signals method.")
