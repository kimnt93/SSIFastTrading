import logging

import pandas as pd

from ssi_trading.models.definitions import DataChannel
from ssi_trading.models.data import CurrentIndex
from ssi_trading.services.stream import BaseDataStream


class IndexDataStream(BaseDataStream[CurrentIndex]):
    def __init__(self, config, list_indexes):
        # the index stream will receive tick data of each market, example:
        """
        {'DataType': 'MI',
        'Content': '{"IndexId":"VN30","IndexValue":1284.46,"PriorIndexValue":1291.3,"TradingDate":"27/06/2024","Time":"10:05:52",
        "TotalTrade":0.0,"TotalQtty":33839600.0,"TotalValue":1103837000000.0,"IndexName":"VN30",
        "Advances":11,"NoChanges":0,"Declines":19,"Ceilings":0,"Floors":0,"Change":-6.84,"RatioChange":-0.53,
        "TotalQttyPt":702391.0,"TotalValuePt":21646000000.0,"Exchange":"HOSE","AllQty":34541991.0,"AllValue":1125483000000.0,
        "IndexType":"","TradingSession":"LO","MarketId":null,"RType":"MI","TotalQttyOd":0.0,"TotalValueOd":0.0}'}
        """
        super().__init__(config, list_indexes, DataChannel.INDEX_DATA)

    def create_instance(self) -> CurrentIndex:
        return CurrentIndex()

    def on_message(self, message):
        # inherit from _BaseStream
        super().on_message(message)
        # process message
        index_name = self._message_content["IndexName"]
        prev = self._current[index_name]
        current = CurrentIndex(
            trading_time=self._message_content["Time"],
            name=index_name,
            current_value=self._message_content["IndexValue"],
            ref_value=self._message_content["PriorIndexValue"],
            total_volume=self._message_content["TotalQtty"],
            total_value=self._message_content["TotalValue"],
            value_change=self._message_content["Change"],
            change_percent=self._message_content["RatioChange"]
        )

        # update current data
        self._current[index_name] = current
        if current.total_volume > prev.total_volume:
            # merge data to dataframe
            new_data = pd.DataFrame([current])
            self._df[index_name] = pd.concat([self._df[index_name], new_data], ignore_index=True)
        else:
            logging.warning("Duplicate or empty index data...")
