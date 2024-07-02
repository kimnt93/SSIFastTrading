from abc import ABC, abstractmethod
from typing import Union, List, Dict

from ssi_fctrading import FCTradingClient
from ssi_trading.config import TradingServiceConfig, DataServiceConfig
from ssi_trading.models.data import StockPrice, DailyIndex, OHLCV
from ssi_trading.models.definitions import OrderStatus, SecurityMarket
from ssi_trading.models.trading import (
    CreatedOrder, AccountBalance, StockPosition, MaxBuySellQty,
)
import requests
from ssi_fc_data import fc_md_client


class BaseDataService(ABC):
    def __init__(self, config: DataServiceConfig):
        self._config: DataServiceConfig = config
        self._client = fc_md_client.MarketDataClient(self._config)

    @abstractmethod
    def stock_price(
            self,
            symbol: str,
            start_date=None, end_date=None,
            page_index: int = 1, page_size: int = 10
    ) -> Union[List[StockPrice], None]:
        raise NotImplementedError()

    @abstractmethod
    def daily_index(
            self, index_id: str,
            start_date=None, end_date=None,
            page_index: int = 1, page_size: int = 10,
            order_by: str = "Tradingdate", ascending: bool = False
    ) -> Union[List[DailyIndex], None]:
        """
        Return daily index info
        :param index_id:
        :param start_date:
        :param end_date:
        :param page_index:
        :param page_size:
        :param order_by:
        :param ascending:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def intraday_ohlcv(
            self, symbol: str,
            start_date=None, end_date=None,
            page_index: int = 1, page_size: int = 10,
            resolution: int = 1,
            ascending: bool = True
    ) -> Union[List[OHLCV], None]:
        """

        :param symbol:
        :param start_date: format dd/mm/yyyy
        :param end_date: format dd/mm/yyyy
        :param page_index: from 1 to 10
        :param page_size: one of 10, 20, 50, 100, 1000
        :param resolution: resample data to 1 eq 1m
        :param ascending:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def daily_ohlcv(
            self, symbol: str,
            start_date=None, end_date=None,
            page_index: int = 1, page_size: int = 10,
            ascending: bool = False
    ) -> Union[List[OHLCV], None]:
        """
        Get daily OHLCV data of a symbol
        :param symbol:
        :param start_date: format dd/mm/yyyy
        :param end_date: format dd/mm/yyyy
        :param page_index: from 1 to 10
        :param page_size: one of 10, 20, 50, 100, 1000
        :param ascending:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def list_index_names(
            self,
            exchange: SecurityMarket.DEFAULT,
            page_index: int = 1, page_size: int = 10
    ) -> Union[List[str], None]:
        """
        Get list of indexes: VN30, VN100, VNALL, HNX30, HNX100, HNXALL, etc.
        :param exchange: HOSE or HNX, if not specify then return all
        :param page_index: 1 to 10
        :param page_size: 10; 20; 50; 100; 1000
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def list_index_components(
            self, index_id: str,
            page_index: int = 1, page_size: int = 100
    ) -> Union[List[str], None]:
        """
        Return all components of an index, example VN30 index return 30 components: ACB, BID, VCB, FPT, etc.
        :param index_id:
        :param page_index: 1 to 10
        :param page_size: one of 10, 20, 50, 100, 500, 1000
        :return:
        """
        raise NotImplementedError()


class BaseTradingService(ABC):
    def __init__(self, config: TradingServiceConfig):
        self._config: TradingServiceConfig = config
        self.account_id: str = self._config.account_id.__str__().upper()
        self._device_id: str = FCTradingClient.get_deviceid()
        self._user_agent: str = FCTradingClient.get_user_agent()
        self._account_token = self._config.auth_token
        if not self._config.paper_trading:
            self._client: FCTradingClient = FCTradingClient(
                self._config.Url, self._config.ConsumerID,
                self._config.ConsumerSecret, "",
                self._config.TwoFAType
            )
        else:
            self._client = requests

        self._market_id = None

    @abstractmethod
    def create_order(self, order: CreatedOrder) -> Union[CreatedOrder, None]:
        raise NotImplementedError()

    @abstractmethod
    def cancel_order(self, order) -> Union[CreatedOrder, None]:
        raise NotImplementedError()

    @abstractmethod
    def modify_order(self, order: CreatedOrder, new_qty: int = 0, new_price: float = 0) -> Union[CreatedOrder, None]:
        raise NotImplementedError()

    @abstractmethod
    def account_balance(self) -> Union[AccountBalance, None]:
        raise NotImplementedError()

    @abstractmethod
    def max_buy_sell_qty(self, symbol, price, order_side) -> Union[MaxBuySellQty, None]:
        raise NotImplementedError()

    @abstractmethod
    def current_positions(self) -> Union[Dict[str, StockPosition], None]:
        raise NotImplementedError()

    @abstractmethod
    def closed_positions(self) -> Union[Dict[str, StockPosition], None]:
        raise NotImplementedError()

    @abstractmethod
    def order_history(self, order_status=None, start_date=None, end_date=None, page=1, page_size=50) -> Union[List[CreatedOrder], None]:
        raise NotImplementedError()

    def pending_orders(self) -> Union[List[CreatedOrder], None]:
        return self.order_history(order_status=",".join(OrderStatus.WORKING_ORDERS))

    def filled_orders(self) -> Union[List[CreatedOrder], None]:
        return self.order_history(order_status=",".join(OrderStatus.FILLED_ORDERS))

    def view_portfolio(self) -> Union[List[StockPosition], None]:
        position_dict = self.current_positions()
        if position_dict is not None:
            return [position_dict[symbol] for symbol in sorted(position_dict.keys())]

        return None

    def current_position(self, symbol: str) -> Union[StockPosition, None]:
        try:
            return self.current_positions().get(symbol, None)
        except KeyError:
            return None

    def closed_position(self, symbol: str) -> Union[StockPosition, None]:
        try:
            return self.closed_positions().get(symbol, None)
        except KeyError:
            return None
