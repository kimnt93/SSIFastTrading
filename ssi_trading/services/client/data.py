import datetime
import logging
from typing import Union, List
from ssi_fc_data import model

from ssi_trading.config import DataServiceConfig
from ssi_trading.models.data import OHLCV, DailyIndex, StockPrice
from ssi_trading.models.definitions import SecurityMarket
from ssi_trading.services.client import BaseDataService
from ssi_trading.utils import ensure_default_ssi_day_format, generate_request_id


class MarketDataService(BaseDataService):
    def stock_price(self, symbol: str, start_date=None, end_date=None, page_index: int = 1,
                    page_size: int = 10) -> Union[List[StockPrice], None]:
        start_date, end_date = ensure_default_ssi_day_format(start_date, end_date)
        try:
            req = model.daily_stock_price(
                symbol=symbol,
                fromDate=start_date,
                toDate=end_date,
                pageIndex=page_index,
                pageSize=page_size,
                market=''
            )
            data = self._client.daily_stock_price(self._config, req)
            if data["status"].lower() == "success":
                return [
                    StockPrice(
                        trading_date=stock_data.get('TradingDate'),
                        price_change=stock_data.get('PriceChange'),
                        per_price_change=stock_data.get('PerPriceChange'),
                        ceiling_price=stock_data.get('CeilingPrice'),
                        floor_price=stock_data.get('FloorPrice'),
                        ref_price=stock_data.get('RefPrice'),
                        open_price=stock_data.get('OpenPrice'),
                        highest_price=stock_data.get('HighestPrice'),
                        lowest_price=stock_data.get('LowestPrice'),
                        close_price=stock_data.get('ClosePrice'),
                        average_price=stock_data.get('AveragePrice'),
                        close_price_adjusted=stock_data.get('ClosePriceAdjusted'),
                        total_match_vol=stock_data.get('TotalMatchVol'),
                        total_match_val=stock_data.get('TotalMatchVal'),
                        total_deal_val=stock_data.get('TotalDealVal'),
                        total_deal_vol=stock_data.get('TotalDealVol'),
                        foreign_buy_vol_total=stock_data.get('ForeignBuyVolTotal'),
                        foreign_current_room=stock_data.get('ForeignCurrentRoom'),
                        foreign_sell_vol_total=stock_data.get('ForeignSellVolTotal'),
                        foreign_buy_val_total=stock_data.get('ForeignBuyValTotal'),
                        foreign_sell_val_total=stock_data.get('ForeignSellValTotal'),
                        total_buy_trade=stock_data.get('TotalBuyTrade'),
                        total_buy_trade_vol=stock_data.get('TotalBuyTradeVol'),
                        total_sell_trade=stock_data.get('TotalSellTrade'),
                        total_sell_trade_vol=stock_data.get('TotalSellTradeVol'),
                        net_buy_sell_vol=stock_data.get('NetBuySellVol'),
                        net_buy_sell_val=stock_data.get('NetBuySellVal'),
                        total_traded_vol=stock_data.get('TotalTradedVol'),
                        total_traded_value=stock_data.get('TotalTradedValue'),
                        symbol=stock_data.get('Symbol'),
                        time=stock_data.get('Time')
                    ) for stock_data in data["data"]
                ]
            else:
                logging.error(f"Error while getting stock price: {data}")
                return None
        except Exception as ex:
            logging.exception(f"Error while getting stock price: {ex}")
            return None

    def daily_index(self, index_id: str, start_date=None, end_date=None, page_index: int = 1, page_size: int = 10,
                    order_by: str = "Tradingdate", ascending: bool = False) -> Union[List[DailyIndex], None]:
        """
        """
        start_date, end_date = ensure_default_ssi_day_format(start_date, end_date)
        try:
            req = model.daily_index(
                requestId=generate_request_id(),
                indexId=index_id,
                fromDate=start_date,
                toDate=end_date,
                pageIndex=page_index,
                pageSize=page_size,
                orderBy=order_by,
                order="desc" if not ascending else "asc"
            )
            data = self._client.daily_index(self._config, req)
            if data["status"].lower() == "success":
                return [
                    DailyIndex(
                        index_id=item.get('IndexId'),
                        index_value=item.get('IndexValue'),
                        trading_date=item.get('TradingDate'),
                        time=item.get('Time'),
                        change=item.get('Change'),
                        ratio_change=item.get('RatioChange'),
                        total_trade=item.get('TotalTrade'),
                        total_match_vol=item.get('TotalMatchVol'),
                        total_match_val=item.get('TotalMatchVal'),
                        type_index=item.get('TypeIndex'),
                        index_name=item.get('IndexName'),
                        advances=item.get('Advances'),
                        no_changes=item.get('NoChanges'),
                        declines=item.get('Declines'),
                        ceilings=item.get('Ceilings'),
                        floors=item.get('Floors'),
                        total_deal_vol=item.get('TotalDealVol'),
                        total_deal_val=item.get('TotalDealVal'),
                        total_vol=item.get('TotalVol'),
                        total_val=item.get('TotalVal'),
                        trading_session=item.get('TradingSession')
                    ) for item in data['data']
                ]
            else:
                logging.error(f"Error while getting daily index: {data}")
                return None
        except Exception as ex:
            logging.exception(f"Error while getting daily index: {ex}")
            return None

    def list_index_components(self, index_id: str, page_index: int = 1, page_size: int = 100) -> Union[List[str], None]:
        try:
            req = model.index_components(
                indexCode=index_id,
                pageIndex=page_index,
                pageSize=page_size
            )
            data = self._client.index_components(self._config, req)
            if data["status"].lower() == "success":
                return [item["StockSymbol"] for item in data['data'][0]['IndexComponent']]
            else:
                logging.error(f"Error while getting list index components: {data}")
                return None
        except Exception as ex:
            logging.exception(f"Error while getting list index components: {ex}")
            return None

    def list_index_names(self, exchange: SecurityMarket.DEFAULT, page_index: int = 1,
                         page_size: int = 10) -> Union[List[str], None]:
        try:
            req = model.index_list(
                exchange=exchange,
                pageIndex=page_index, pageSize=page_size
            )
            data = self._client.index_list(self._config, req)
            if data["status"].lower() == "success":
                return [item["IndexCode"] for item in data['data']]
            else:
                return None
        except Exception as ex:
            logging.exception(f"Error while getting list index names: {ex}")
            return None

    def intraday_ohlcv(self, symbol: str, start_date=None, end_date=None, page_index: int = 1, page_size: int = 10,
                       resolution: int = 1, ascending: bool = True) -> Union[List[OHLCV], None]:
        start_date, end_date = ensure_default_ssi_day_format(start_date, end_date)
        try:
            req = model.intraday_ohlc(
                symbol=symbol,
                fromDate=start_date, toDate=end_date,
                pageSize=page_index, pageIndex=page_size,
                ascending=ascending,
                resolution=resolution
            )
            data = self._client.intraday_ohlc(self._config, req)
            if data["status"].lower() == "success":
                return [
                    OHLCV(
                        symbol=item["Symbol"],
                        trading_time=datetime.datetime.strptime(f'{item["TradingDate"]} {item["Time"]}', "%d/%m/%Y %H:%M:%S"),
                        open=item["Open"],
                        high=item["High"],
                        low=item["Low"],
                        close=item["Close"],
                        volume=item["Volume"],
                        value=item["Value"],
                    ) for item in data['data']
                ]
            else:
                logging.error(f"Error while getting intraday ohlcv: {data}")
                return None
        except Exception as ex:
            logging.exception(f"Error while getting intraday ohlcv: {ex}")
            return None

    def daily_ohlcv(self, symbol: str, start_date=None, end_date=None, page_index: int = 1, page_size: int = 10,
                    ascending: bool = False) -> Union[List[OHLCV], None]:

        start_date, end_date = ensure_default_ssi_day_format(start_date, end_date)
        try:
            req = model.daily_ohlc(symbol, start_date, end_date, page_index, page_size, ascending)
            data = self._client.daily_ohlc(self._config, req)
            if data["status"].lower() == "success":
                return [
                    OHLCV(
                        symbol=item["Symbol"],
                        trading_time=datetime.datetime.strptime(item["TradingDate"], "%d/%m/%Y"),
                        open=item["Open"],
                        high=item["High"],
                        low=item["Low"],
                        close=item["Close"],
                        volume=item["Volume"],
                        value=item["Value"],
                    ) for item in data['data']
                ]
            else:
                logging.error(f"Error while getting daily ohlcv: {data}")
                return None
        except Exception as ex:
            logging.exception(f"Error while getting list index names: {ex}")
            return None

    def __init__(self, config: DataServiceConfig):
        super().__init__(config)
