import logging

import pandas as pd

from ssi_trading.models.definitions import DataChannel
from ssi_trading.models.data import CurrentForeignRoom
from ssi_trading.services.stream import BaseDataStream


class ForeignRoomDataStream(BaseDataStream[CurrentForeignRoom]):
    def __init__(self, config, list_symbols):
        # the bar stream will receive OHLCV, example:
        """
        { datatype: 'R',
        content:
        '{"RType":"R","TradingDate":"04/05/2020","Time":"15:02:45","Isin":"YTC","Symbol":"YTC","TotalRoom":0.
        0,"CurrentRoom":1475400.0,"BuyVol":0.0,"SellVol":0.0,"BuyVal":0.0,"SellVal":0.0,"MarketId":"UPCOM","E
        xchange":"UPCOM"}' }
        """
        super().__init__(config, list_symbols, DataChannel.FR_ROOM_DATA)

    def create_instance(self) -> CurrentForeignRoom:
        return CurrentForeignRoom()

    def on_message(self, message):
        # inherit from _BaseStream
        super().on_message(message)
        # process message
        symbol = self._message_content["Symbol"]
        prev = self._current[symbol]
        current = CurrentForeignRoom(
            trading_time=self._message_content["Time"],
            symbol=symbol,
            total_room=self._message_content["TotalRoom"],
            current_room=self._message_content["CurrentRoom"],
            buy_volume=self._message_content["BuyVol"],
            sell_volume=self._message_content["SellVol"],
            buy_value=self._message_content["BuyVal"],
            sell_value=self._message_content["SellVal"],
        )

        # update current data
        self._current[symbol] = current
        if current.buy_volume > prev.buy_volume and current.sell_volume > prev.sell_volume:
            # merge data to dataframe
            new_data = pd.DataFrame([current])
            self._df[symbol] = pd.concat([self._df[symbol], new_data], ignore_index=True)
        else:
            logging.warning("Duplicate or empty index data...")
