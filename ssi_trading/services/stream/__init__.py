import json
import logging
from typing import Union, List, Dict, Generic, TypeVar
import sys

from pandas import DataFrame
from ssi_fc_data.fc_md_client import MarketDataClient
from ssi_fc_data.fc_md_stream import MarketDataStream
from ssi_fctrading import FCTradingClient, FCTradingStream

from vn_trading.config import StreamServiceConfig, TradingServiceConfig

data_logger = logging.getLogger("data")
data_logger.setLevel(logging.DEBUG)

# Create a file handler that logs only DEBUG level messages
file_handler = logging.FileHandler('data.log')
file_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the trading logger
data_logger.addHandler(file_handler)


# Add a filter to skip other log levels if necessary (optional)
class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG


file_handler.addFilter(DebugFilter())


T = TypeVar("T")


class BaseTradingStream(Generic[T]):
    def __init__(self, config: TradingServiceConfig, account_id: str):
        self.account_id = account_id
        self._config = config
        self._client = FCTradingClient(
            self._config.Url, self._config.ConsumerID,
            self._config.ConsumerSecret, self._config.PrivateKey,
            self._config.TwoFAType
        )
        self._streamer: Union[FCTradingStream, None] = None

    def on_message(self, message):
        logging.info(message)

    def on_error(self, error):
        logging.error(f"Stream {self._config.StreamURL} problem. Error while receiving message: {error}")
        sys.exit(1)

    def start_stream(self):
        if self._streamer is None:
            # stream channel
            self._streamer = FCTradingStream(
                fctrading_client=self._client,
                stream_url=self._config.StreamURL,
                last_notify_id=self._config.NotifyId.__str__(),
                on_message=self.on_message,
                on_error=self.on_error
            )
            logging.info(f"Start stream : {self._config.StreamURL}")
            self._streamer.start()
        else:
            logging.warning("Data stream is already started.")


class BaseDataStream(Generic[T]):
    def __init__(self, config: StreamServiceConfig, names: List[str], channel_name: str):
        """
        :param config: DataServiceConfig instance
        :param names: VN30, VN30F2407, HPG, etc.
        :param channel_name: X, F, MI, etc.
        """
        self._config = config
        self._names = names
        self._names = names if isinstance(names, list) else [names]
        self._names = [name for name in self._names if name is not None]
        if "ALL" in self._names:
            raise ValueError("Index names must be provided or not equal to 'ALL'")

        self.channel_name = channel_name
        self._streamer: Union[MarketDataStream, None] = None

        self._df: Dict[str, DataFrame] = dict()
        self._current: Dict[str, T] = dict()
        # init
        for index_name in self._names:
            self._df[index_name] = DataFrame()
            self._current[index_name] = self.create_instance()

        # store message
        self._message_type = None
        self._message_content = None

    def get_dataframe(self, symbol) -> DataFrame:
        return self._df.get(symbol, DataFrame())

    def get_current(self, symbol) -> T:
        return self._current.get(symbol, None)

    def create_instance(self):
        raise NotImplementedError("Method create_instance is not implemented yet.")

    def on_message(self, message):
        data_logger.debug(f"Recv message: {message}")
        message = json.loads(message) if isinstance(message, str) else message
        self._message_content = json.loads(message["Content"]) if isinstance(message["Content"], str) else message["Content"]
        self._message_type = message['DataType']

    def on_error(self, error):
        logging.error(f"Channel {self.channel_name} problem. Error while receiving message: {error}")
        sys.exit(1)

    def start_stream(self):
        if len(self._names) == 0:
            logging.warning("No symbol is provided. Skip starting price stream.")
        else:
            if self._streamer is None:
                # stream channel
                self._streamer = MarketDataStream(self._config, MarketDataClient(self._config))
                channel = f"{self.channel_name}:{'-'.join(self._names)}"
                logging.info(f"Start stream with channel: {channel}")
                self._streamer.start(self.on_message, self.on_error, channel)
            else:
                logging.warning("Data stream is already started.")
        return self

