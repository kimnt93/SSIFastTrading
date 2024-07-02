import logging

import pandas as pd

from ssi_trading.models.definitions import DataChannel
from ssi_trading.models.data import CurrentMarket
from ssi_trading.services.stream import BaseDataStream


class MarketDataStream(BaseDataStream[CurrentMarket]):
    def __init__(self, config):
        # the price stream will receive tick data of each symbol, example:
        """
        {'DataType': 'X',
        'Content': '{"RType":"X","TradingDate":"27/06/2024","Time":"09:43:41","Isin":"VN30F2407",
        "Symbol":"VN30F2407","Ceiling":1380.3,"Floor":1199.7,"RefPrice":1290.0,"Open":1285.0,"High":1287.0,"Low":1282.0,"Close":1283.9,
        "AvgPrice":128454615.60380691,"PriorVal":1290.0,"LastPrice":1283.9,"LastVol":8.0,"TotalVal":4507986280000.0,"TotalVol":35094.0,
        "BidPrice1":1283.8,"BidPrice2":1283.7,"BidPrice3":1283.6,"BidPrice4":1283.5,"BidPrice5":1283.4,"BidPrice6":1283.3,"BidPrice7":1283.2,"BidPrice8":1283.1,"BidPrice9":1283.0,"BidPrice10":1282.9,
        "BidVol1":47.0,"BidVol2":89.0,"BidVol3":10.0,"BidVol4":34.0,"BidVol5":44.0,"BidVol6":101.0,"BidVol7":18.0,"BidVol8":29.0,"BidVol9":209.0,"BidVol10":130.0,
        "AskPrice1":1283.9,"AskPrice2":1284.0,"AskPrice3":1284.1,"AskPrice4":1284.2,"AskPrice5":1284.3,"AskPrice6":1284.4,"AskPrice7":1284.5,"AskPrice8":1284.6,"AskPrice9":1284.7,"AskPrice10":1284.8,
        "AskVol1":125.0,"AskVol2":182.0,"AskVol3":159.0,"AskVol4":4.0,"AskVol5":7.0,"AskVol6":23.0,"AskVol7":132.0,"AskVol8":39.0,"AskVol9":19.0,"AskVol10":68.0,
        "MarketId":"DERIVATIVES","Exchange":"DERIVATIVES","TradingSession":"LO","TradingStatus":"Active",
        "Change":-6.099999999999909,"RatioChange":-0.47,"EstMatchedPrice":1283.9,"Side":null,"CloseQtty":0.0}'}
        """
        super().__init__(config, config.symbols, DataChannel.MARKET_DATA)

    def create_instance(self) -> CurrentMarket:
        return CurrentMarket()

    def on_message(self, message):
        # inherit from _BaseStream
        super().on_message(message)
        # process message
        symbol = self._message_content["Symbol"]
        prev = self._current[symbol]
        current = CurrentMarket(
            trading_time=self._message_content["Time"],
            symbol=symbol,
            current_price=self._message_content["LastPrice"],
            current_volume=self._message_content["LastVol"],
            total_volume=self._message_content["TotalVol"],
            ref_price=self._message_content["RefPrice"],
            ceiling_price=self._message_content["Ceiling"],
            floor_price=self._message_content["Floor"],
            open_price=self._message_content["Open"],
            high_price=self._message_content["High"],
            low_price=self._message_content["Low"],
            avg_price=self._message_content["AvgPrice"],
            bid_price_01=self._message_content["BidPrice1"],
            bid_volume_01=self._message_content["BidVol1"],
            ask_price_01=self._message_content["AskPrice1"],
            ask_volume_01=self._message_content["AskVol1"],
            price_change=self._message_content["Change"],
            change_percent=self._message_content["RatioChange"]
        )

        # update current data
        self._current[symbol] = current
        if current.total_volume > prev.total_volume and current.current_volume != 0:
            # merge data to dataframe
            new_data = pd.DataFrame([current])
            self._df[symbol] = pd.concat([self._df[symbol], new_data], ignore_index=True)
        else:
            logging.warning("Duplicate or empty tick data...")
