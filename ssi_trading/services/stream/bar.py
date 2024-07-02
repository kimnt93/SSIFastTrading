import logging

import pandas as pd

from ssi_trading.models.definitions import DataChannel
from ssi_trading.models.data import CurrentBar
from ssi_trading.services.stream import BaseDataStream


class BarDataStream(BaseDataStream[CurrentBar]):
    def __init__(self, config):
        # the bar stream will receive OHLCV, example:
        """
        {‘Datatype’: 'B',
        ‘Content’: '{"RType":"B","Symbol":"X26","TradingTime":"14:28:33",
        "Open":16000,"High":16000,"Low":16000,"Close":16000,"Volume":5000,"Value":0}'}
        """
        super().__init__(config, config.symbols, DataChannel.BAR_DATA)

    def create_instance(self) -> CurrentBar:
        return CurrentBar()

    def on_message(self, message):
        # inherit from _BaseStream
        super().on_message(message)
        # process message
        symbol = self._message_content["Symbol"]
        prev = self._current[symbol]
        current = CurrentBar(
            trading_time=self._message_content["Time"],
            symbol=symbol,
            open=self._message_content["Open"],
            high=self._message_content["High"],
            low=self._message_content["Low"],
            close=self._message_content["Close"],
            volume=self._message_content["Volume"],
            value=self._message_content["Value"]
        )

        # update current data
        self._current[symbol] = current
        if current.volume > prev.volume:
            # merge data to dataframe
            new_data = pd.DataFrame([current])
            self._df[symbol] = pd.concat([self._df[symbol], new_data], ignore_index=True)
        else:
            logging.warning("Duplicate or empty index data...")
