import datetime
from dataclasses import dataclass, field
from typing import List


@dataclass
class CurrentMarket:
    trading_time: str = ""
    symbol: str = ""
    current_price: float = 0.0
    current_volume: float = 0.0
    total_volume: float = 0.0
    price_change: float = 0.0
    change_percent: float = 0.0
    ref_price: float = 0.0
    ceiling_price: float = 0.0
    floor_price: float = 0.0
    open_price: float = 0.0
    high_price: float = 0.0
    low_price: float = 0.0
    avg_price: float = 0.0
    bid_price_01: float = 0.0
    bid_volume_01: float = 0.0
    ask_price_01: float = 0.0
    ask_volume_01: float = 0.0


@dataclass
class CurrentIndex:
    trading_time: str = ""
    name: str = ""
    current_value: float = 0.0
    ref_value: float = 0.0
    total_volume: float = 0.0
    total_value: float = 0.0
    value_change: float = 0.0
    change_percent: float = 0.0


@dataclass
class CurrentBar:
    symbol: str = ""
    trading_time: str = ""
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0.0
    value: float = 0.0


@dataclass
class CurrentForeignRoom:
    symbol: str = ""
    trading_time: str = ""
    total_room: float = 0.0
    current_room: float = 0.0
    buy_volume: float = 0.0
    sell_volume: float = 0.0
    buy_value: float = 0.0
    sell_value: float = 0.0


@dataclass
class SecurityInfo:
    market: str
    symbol: str
    stock_name: str
    stock_en_name: str


@dataclass
class OHLCV:
    symbol: str
    trading_time: datetime.datetime  # 14/06/2024 -> 2024-06-14 00:00:00
    open: float
    high: float
    low: float
    close: float
    volume: float
    value: float


@dataclass
class DailyIndex:
    index_id: str
    index_value: str
    trading_date: str
    time: str
    change: str
    ratio_change: str
    total_trade: str
    total_match_vol: str
    total_match_val: str
    type_index: str
    index_name: str
    advances: str
    no_changes: str
    declines: str
    ceilings: str
    floors: str
    total_deal_vol: str
    total_deal_val: str
    total_vol: str
    total_val: str
    trading_session: str


@dataclass
class StockPrice:
    trading_date: str
    price_change: str
    per_price_change: str
    ceiling_price: str
    floor_price: str
    ref_price: str
    open_price: str
    highest_price: str
    lowest_price: str
    close_price: str
    average_price: str
    close_price_adjusted: str
    total_match_vol: str
    total_match_val: str
    total_deal_val: str
    total_deal_vol: str
    foreign_buy_vol_total: str
    foreign_current_room: str
    foreign_sell_vol_total: str
    foreign_buy_val_total: str
    foreign_sell_val_total: str
    total_buy_trade: str
    total_buy_trade_vol: str
    total_sell_trade: str
    total_sell_trade_vol: str
    net_buy_sell_vol: str
    net_buy_sell_val: str
    total_traded_vol: str
    total_traded_value: str
    symbol: str
    time: str
