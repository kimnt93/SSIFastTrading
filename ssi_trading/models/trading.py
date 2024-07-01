from dataclasses import dataclass
from typing import Union, Optional

from ssi_trading.models.definitions import OrderSide, OrderType, StopOrderType


@dataclass
class CreatedOrder:
    symbol: str
    market_id: str
    account_id: str
    order_side: str
    order_type: str
    order_price: float
    order_qty: int
    # response should be added
    order_id: Optional[str] = None
    order_status: Optional[None] = None
    # stop order for futures
    stop_order: Optional[bool] = False
    stop_price: Optional[float] = 0
    stop_type: Optional[str] = StopOrderType.DEFAULT
    stop_step: Optional[float] = 0
    loss_step: Optional[float] = 0
    profit_step: Optional[float] = 0
    # using for history
    avg_price: Optional[float] = 0
    os_qty: Optional[int] = 0
    filled_qty: Optional[int] = 0


@dataclass
class StockPosition:
    symbol: str
    market_id: str
    account_id: str
    position: str
    trading_pl: Optional[float] = None
    floating_pl: Optional[float] = None
    market_price: Optional[float] = None
    avg_price: Optional[float] = None


@dataclass
class AccountBalance:
    balance: str
    market_id: str
    account_id: str
    trading_pl: Optional[float] = None
    floating_pl: Optional[float] = None
    total_pl: Optional[float] = None
    ee: Optional[float] = None
    nav: Optional[float] = None
    withdrawable: Optional[float] = None
    fee: Optional[float] = None
    interest: Optional[float] = None
    commission: Optional[float] = None


@dataclass
class MaxBuySellQty:
    market_id: str
    account_id: str
    symbol: str
    max_qty: str
    power: Optional[float] = None

