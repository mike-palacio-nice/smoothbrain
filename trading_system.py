import threading
from abc import abstractmethod, ABC
from alpaca_trade_api import REST, TimeFrame

class AlpacaInterface(REST):
    def __init__(self, key_id, secret_key, base_url):
        super().__init__(
            key_id=key_id,
            secret_key=secret_key,
            base_url=base_url
        )

class TradingSystem(ABC):

    def __init__(self, api, symbol, time_frame, system_id, system_label):
        self.api = api
        self.symbol = symbol
        self.time_frame = time_frame
        self.system_id = system_id
        self.system_label = system_label
        thread = threading.Thread(target=self.system_loop)
        thread.start()

    @abstractmethod
    def place_buy_order(self):
        pass

    @abstractmethod
    def place_sell_order(self):
        pass

    @abstractmethod
    def system_loop(self):
        pass

if __name__ == "__main__":
    api = AlpacaInterface(
        key_id='CKS4IVTTT5PASLF1OLOJ',
        secret_key='t8o5E3vlrJkKxmLXNXoh00DOvMngiqUH2sw2gtpc',
        base_url='https://paper-api.alpaca.markets',
    )
    api.get_bars("AAPL", TimeFrame.Hour, "2021-06-08", "2021-06-08", adjustment='raw').df