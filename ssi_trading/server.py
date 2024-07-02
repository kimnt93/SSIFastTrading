import logging
from typing import TypeVar, Generic, Dict, Union, List

from pandas import DataFrame

from ssi_trading.exceptions import TradingServiceUnavailable
from ssi_trading.models.data import (
    CurrentBar, CurrentIndex, CurrentMarket, CurrentForeignRoom,
    OHLCV, DailyIndex, StockPrice
)
from ssi_trading.models.definitions import DataChannel
from ssi_trading.models.trading import CreatedOrder, AccountBalance, StockPosition, MaxBuySellQty
from ssi_trading.services.client import BaseTradingService, BaseDataService
from ssi_trading.services.stream import BaseDataStream, BaseTradingStream


TDataStream = TypeVar('TDataStream', bound=BaseDataStream)
TDataService = TypeVar('TDataService', bound=BaseDataService)

TTradingService = TypeVar('TTradingService', bound=BaseTradingService)
TTradingStream = TypeVar('TTradingStream', bound=BaseTradingStream)


class SSIServices(Generic[TDataStream, TTradingStream, TTradingService, TDataService]):
    def __init__(self):
        self._data_streams: Dict[str, TDataStream] = dict()
        self._data_service: Union[TDataService, None] = None

        self._trading_streams: Dict[str, TTradingStream] = dict()
        self._trading_services: Dict[str, TTradingService] = dict()

    # region setup stream, services
    #
    def add_data_stream(self, stream: TDataStream):
        self._data_streams[stream.channel_name] = stream
        return self

    def add_trading_steam(self, stream: TTradingStream):
        self._trading_streams[stream.account_id] = stream
        return self

    def add_trading_service(self, service: TTradingService):
        self._trading_services[service.account_id] = service
        return self

    def add_data_service(self, service: TDataService):
        self._data_service = service
        return self

    def start_data_stream(self):
        for stream in self._data_streams.values():
            logging.debug(f"Start data stream: {stream}")
            stream.start_stream()
        return self

    def start_trading_stream(self):
        for stream in self._trading_streams.values():
            logging.debug(f"Start trading stream: {stream}")
            stream.start_stream()
        return self
    # endregion

    # region trading services
    # create, cancel, modify, account_balance, current_positions,
    # closed_positions, max_buy_sell_qty, order_history, etc.
    def create_order(self, order: CreatedOrder) -> Union[CreatedOrder, None]:
        if order.account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {order.account_id} is not available.")
        return self._trading_services[order.account_id].create_order(order)

    def cancel_order(self, order) -> Union[CreatedOrder, None]:
        if order.account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {order.account_id} is not available.")
        return self._trading_services[order.account_id].cancel_order(order)

    def modify_order(self, order: CreatedOrder, new_qty: int = 0, new_price: float = 0) -> CreatedOrder:
        if order.account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {order.account_id} is not available.")
        return self._trading_services[order.account_id].modify_order(order, new_qty, new_price)

    def account_balance(self, account_id) -> Union[AccountBalance, None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].account_balance()

    def current_position(self, account_id, symbol: str) -> Union[StockPosition, None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].current_position(symbol)

    def current_positions(self, account_id) -> Union[List[StockPosition], None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].current_positions()

    def closed_position(self, account_id, symbol: str) -> Union[StockPosition, None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].closed_position(symbol)

    def closed_positions(self, account_id) -> Union[List[StockPosition], None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].closed_positions()

    def max_buy_sell_qty(self, account_id, symbol, price, order_side) -> Union[MaxBuySellQty, None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].max_buy_sell_qty(symbol, price, order_side)

    def order_history(self, account_id) -> Union[List[CreatedOrder], None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].order_history(order_status=None, start_date=None, end_date=None, page=1, page_size=50)

    def pending_orders(self, account_id) -> Union[List[CreatedOrder], None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].pending_orders()

    def filled_orders(self, account_id) -> Union[List[CreatedOrder], None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].filled_orders()

    def view_portfolio(self, account_id) -> Union[List[StockPosition], None]:
        if account_id not in self._trading_services:
            raise TradingServiceUnavailable(f"Account ID {account_id} is not available.")
        return self._trading_services[account_id].view_portfolio()

    # endregion

    # region data stream services
    # get_dataframe, get_current, get_current_bar_from_stream, get_df_bar_from_stream, etc.
    # if channel has not been added, raise ValueError
    #
    def get_df_bar_from_stream(self, symbol) -> DataFrame:
        if DataChannel.BAR_DATA not in self._data_streams:
            raise ValueError("Bar data stream is not available.")
        return self._data_streams[DataChannel.BAR_DATA].get_dataframe(symbol)

    def get_current_bar_from_stream(self, symbol) -> CurrentBar:
        if DataChannel.BAR_DATA not in self._data_streams:
            raise ValueError("Bar data stream is not available.")
        return self._data_streams[DataChannel.BAR_DATA].get_current(symbol)

    def get_df_foreign_from_stream(self, symbol) -> DataFrame:
        if DataChannel.FR_ROOM_DATA not in self._data_streams:
            raise ValueError("Foreign data stream is not available.")
        return self._data_streams[DataChannel.FR_ROOM_DATA].get_dataframe(symbol)

    def get_current_foreign_from_stream(self, symbol) -> CurrentForeignRoom:
        if DataChannel.FR_ROOM_DATA not in self._data_streams:
            raise ValueError("Foreign data stream is not available.")
        return self._data_streams[DataChannel.FR_ROOM_DATA].get_current(symbol)

    def get_df_index_from_stream(self, symbol) -> DataFrame:
        if DataChannel.INDEX_DATA not in self._data_streams:
            raise ValueError("Index data stream is not available.")
        return self._data_streams[DataChannel.INDEX_DATA].get_dataframe(symbol)

    def get_current_index_from_stream(self, symbol) -> CurrentIndex:
        if DataChannel.INDEX_DATA not in self._data_streams:
            raise ValueError("Index data stream is not available.")
        return self._data_streams[DataChannel.INDEX_DATA].get_current(symbol)

    def get_df_market_from_stream(self, symbol) -> DataFrame:
        if DataChannel.MARKET_DATA not in self._data_streams:
            raise ValueError("Market data stream is not available.")
        return self._data_streams[DataChannel.MARKET_DATA].get_dataframe(symbol)

    def get_current_market_from_stream(self, symbol) -> CurrentMarket:
        if DataChannel.MARKET_DATA not in self._data_streams:
            raise ValueError("Market data stream is not available.")
        return self._data_streams[DataChannel.MARKET_DATA].get_current(symbol)

    # endregion
    # region dataservices
    # daily_index, daily_ohlcv, intraday_ohlcv, list_index_components, list_index_names, stock_price, etc.
    def daily_index(self, index_name, start_date, end_date) -> Union[List[DailyIndex], None]:
        return self._data_service.daily_index(index_name, start_date, end_date)

    def daily_ohlcv(self, symbol, start_date, end_date) -> Union[List[OHLCV], None]:
        return self._data_service.daily_ohlcv(symbol, start_date, end_date)

    def intraday_ohlcv(self, symbol, start_date, end_date) -> Union[List[OHLCV], None]:
        return self._data_service.intraday_ohlcv(symbol, start_date, end_date)

    def list_index_components(self, index_name) -> Union[List[str], None]:
        return self._data_service.list_index_components(index_name)

    def list_index_names(self, exchange) -> Union[List[str], None]:
        return self._data_service.list_index_names(exchange)

    def stock_price(self, symbol, start_date, end_date) -> Union[List[StockPrice], None]:
        return self._data_service.stock_price(symbol, start_date, end_date)

    # endregion
